import pypdf
import requests
from io import BytesIO


class PdfReader:
    def __init__(self) -> None:
        pass

    def download_pdf(self, url: str) -> BytesIO:
        """Download PDF file from a URL."""
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return BytesIO(response.content)

    def read_pdf(self, file_path_or_url: str) -> str:
        """Extract text from a PDF file or URL."""
        text = ""
        try:
            if file_path_or_url.startswith("http://") or file_path_or_url.startswith(
                "https://"
            ):
                file = self.download_pdf(file_path_or_url)
            else:
                file = open(file_path_or_url, "rb")

            with file:
                reader = pypdf.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"  # Add a newline for separation
        except Exception as e:
            print(f"Error reading {file_path_or_url}: {e}")
        return text.strip()  # Remove leading/trailing whitespace
