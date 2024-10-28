import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from src.matcher.matcher import Matcher
from src.preprocessing.pdf_reader import PdfReader
from src.preprocessing.docx_reader import DocxReader
from src.utils.aws_utilities import fetch_all_keys_from_s3

# For reading DOCX files
from src.preprocessing.preprocess import Preprocess

load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Define the origins that should be allowed to make requests to your API
origins = [
    "http://localhost:5173",  # Add your frontend URL here
    "http://resumejdmatcherfe.s3-website.ap-south-1.amazonaws.com",
]

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

pdf_reader = PdfReader()


# Define the request model
class MatchRequest(BaseModel):
    job_description: Optional[str] = Field(None)


@app.get("/")
async def ping():
    return {"message": "Welcome to the Resume Matcher API!"}


@app.post("/match")
async def match(request: MatchRequest):

    # Fetch all resume files from the S3 bucket
    print("Fetching all resume files from S3 bucket")
    resume_files = fetch_all_keys_from_s3(
        os.environ["RESUME_S3_BUCKET_NAME"],
        os.environ["AWS_ACCESS_KEY_ID"],
        os.environ["AWS_SECRET_ACCESS_KEY"],
        os.environ["AWS_DEFAULT_REGION"],
    )
    # Replace whitespace with %20 in the file names
    resume_files = [file.replace(" ", "%20") for file in resume_files]

    # Check if the job description is provided
    if request.job_description is None:
        # Get the job description key from the S3 bucket
        job_desc_key = fetch_all_keys_from_s3(
            os.environ["JOB_DESCRIPTION_S3_BUCKET_NAME"],
            os.environ["AWS_ACCESS_KEY_ID"],
            os.environ["AWS_SECRET_ACCESS_KEY"],
            os.environ["AWS_DEFAULT_REGION"],
        )[0]

        # Fetch the job description from the S3 bucket
        print(f"Fetching job description from S3")
        job_desc_path = (
            "https://"
            + os.environ["JOB_DESCRIPTION_S3_BUCKET_NAME"]
            + ".s3."
            + os.environ["AWS_DEFAULT_REGION"]
            + ".amazonaws.com/"
            + job_desc_key
        )

        # Read the job description text
        job_desc_text = pdf_reader.read_pdf(job_desc_path)
    else:
        job_desc_text = request.job_description

    # doc_reader = DocReader()
    docx_reader = DocxReader()

    # List to store similarity scores
    similarity_scores = {}

    # Process each resume
    for resume_file in resume_files:
        resume_path = (
            "https://"
            + os.environ["RESUME_S3_BUCKET_NAME"]
            + ".s3."
            + os.environ["AWS_DEFAULT_REGION"]
            + ".amazonaws.com/"
            + resume_file
        )

        # Read the resume text based on its extension
        if resume_file.endswith(".pdf"):
            print(f"Reading PDF: {resume_file}")
            resume_text = pdf_reader.read_pdf(resume_path)

        elif resume_file.endswith(".docx"):
            resume_text = docx_reader.read_docx(resume_path)

        # Initialize the preprocessor and matcher
        processor = Preprocess()
        corpus = [resume_text, job_desc_text]  # Start with the job description

        # Fit the vectorizer on the job description
        processor.fit_vectorizer(corpus)

        # Preprocess the resume
        resume_vector = processor.preprocess(resume_text)
        job_desc_vector = processor.preprocess(job_desc_text)

        # Calculate similarity
        matcher = Matcher()
        score = matcher.compute_similarity(resume_vector, job_desc_vector)

        # Remove .pdf from resume file name
        resume_file = resume_file.replace(".pdf", "")
        resume_file = resume_file.replace("%20", " ")

        # Store the score and resume url in the dictionary
        similarity_scores[resume_file] = {"url": resume_path, "score": score}

    # Return the scores
    return similarity_scores
