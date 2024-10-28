<template>
  <div variant="flat" class="pl-10 pt-5 ma-0">
    <v-img
      src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Vue.js_Logo_2.svg/512px-Vue.js_Logo_2.svg.png"
      height="80px"
      width="150px"
    ></v-img>
  </div>
  <div
    class="banner-wrapper"
    style="
      background: linear-gradient(
        90deg,
        rgba(34, 193, 195, 1) 50%,
        rgba(45, 126, 253, 1) 100%
      );
    "
  >
    <v-container>
      <input
        ref="fileInputRef"
        type="file"
        style="display: none"
        multiple
        @change="handleFileUpload($event)"
      />

      <input
        ref="jDFileInputRef"
        type="file"
        style="display: none"
        @change="handleJdFileUpload($event)"
      />
      <v-row justify="center">
        <v-col cols="12" md="7" lg="6" xl="5" class="d-flex align-center">
          <div class="text-center text-md-left">
            <h1 class="banner-title font-weight-bold text-white text-h2">
              Smart Resume Matcher
            </h1>
            <h4 class="banner-subtitle text-white font-weight-regular">
              Upload Resumes and Instantly Compare with Job Description.
              <v-tooltip
                width="300"
                color="white"
                bg-color="primary"
                content-class="custom-tooltip "
              >
                <template v-slot:activator="{ props }">
                  <v-btn
                    size="x-small"
                    icon
                    variant="text"
                    v-bind="props"
                    class="px-0 mx-0"
                    ><v-icon size="large"
                      >mdi-information-variant-circle-outline</v-icon
                    ></v-btn
                  >
                </template>
                <template v-slot:default>
                  <div class="pt-2 text-black">
                    We will match your resume with your job description based on keywords
                    and skills that you have listed. Our algorithm will match your resumes
                    with your job description
                  </div>
                </template>
              </v-tooltip>
            </h4>
            <div class="">
              <v-btn
                v-if="!jDFile"
                color="white"
                class="px-0 text-capitalize text-h6 font-weight-bold"
                large
                variant="text"
                size="large"
                :disabled="jDFile || jobDescription ? true : false"
                elevation="0"
                @click="openJdFileInput()"
              >
                {{ jDFile ? "JD uploaded ✔" : " click here upload JD file" }}
              </v-btn>
              <div v-else class="px-0 text-capitalize text-h6 text-white">
                JD uploaded ✔
                <v-btn variant="text" @click="jDFile = null"
                  ><v-icon size="large">mdi-close</v-icon></v-btn
                >
              </div>
              <div class="text-white text-h6 text-center mx-3">Or</div>
              <br />
              <v-textarea
                v-model="jobDescription"
                rounded="xl"
                clearable
                rows="3"
                auto-grow
                variant="outlined"
                :disabled="jDFile ? true : false"
                class="text-white"
              >
                <template #label>
                  <div class="text-white font-weight-bold text-h6">
                    Paste your Job Description here..
                  </div>
                </template>
              </v-textarea>
            </div>
            <p class="text-white">Note:</p>
            <ul class="text-white px-12">
              <li>you can upload multiple resumes</li>
              <li>only .pdf format files are accepted</li>
            </ul>
            <div class="mt-4 pt-2">
              <v-btn
                color="error"
                class="mr-0 mr-md-8 mb-5 mb-md-0 text-capitalize text-h6"
                large
                size="large"
                target="_blank"
                elevation="0"
                @click="openFileInput()"
              >
                upload Resume files
              </v-btn>
              <v-btn
                size="large"
                variant="outlined"
                class="mr-0 mr-md-8 mb-5 mb-md-0 text-capitalize text-h6"
                outlined
                color="white"
                elevation="0"
                @click="resumeAnalysis()"
              >
                Resume Analysis
              </v-btn>
            </div>
            <p v-if="uploadedFiles" class="text-white mt-1">
              <v-icon size="x-small" class="mr-1"> mdi-check-circle-outline</v-icon
              >{{ uploadedFiles ? `${uploadedFiles.length} Files uploaded ` : "" }}
            </p>
          </div>
        </v-col>
        <v-col cols="12" md="5" lg="6">
          <v-img :src="bannerImg" alt="banner" class="animated-image" />
        </v-col>
      </v-row>
    </v-container>
  </div>

  <div
    v-if="items.length > 0"
    class="px-16 mb-4 d-flex align-center justify-space-between"
  >
    <div class="d-flex align-center justify-space-between" style="width: 50% !important">
      <h1 class="text-white">Detailed Match Scores</h1>
      <!-- <v-text-field
        v-model="search"
        append-inner-icon="mdi-magnify"
        variant="solo"
        class="mx-2"
        density="compact"
        label="Search"
        single-line
        hide-details
      ></v-text-field> -->
    </div>
    <!-- <div>
      <v-menu location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn color="white" icon size="small" variant="outlined" dark v-bind="props">
            <v-icon>mdi-filter-menu</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="(item, index) in selectRange" :key="index">
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div> -->
  </div>

  <div>
    <v-row class="px-16">
      <v-col
        v-for="(item, index) in paginatedItems"
        :key="index"
        cols="12"
        sm="6"
        md="3"
        lg="3"
        xl="3"
      >
        <v-card
          class="mx-auto"
          max-width="500"
          flat
          style="border-radius: 16px"
          elevation="1"
        >
          <v-list-item class="px-6" height="88">
            <template v-slot:prepend>
              <v-avatar color="surface-light" size="32">🎯</v-avatar>
            </template>

            <template v-slot:title>
              <span class="font-weight-bold"> FileName </span>
            </template>
            <template v-slot:subtitle>
              <span class="font-weight-bold"> {{ item.fileName }} </span>
            </template>
          </v-list-item>

          <v-divider></v-divider>

          <v-card-text class="text-medium-emphasis pa-6">
            <div class="text-h4 font-weight-black mb-4">
              {{ item.match }} <span class="text-caption"> Match </span>
            </div>

            <v-progress-linear
              bg-color="surface-variant"
              class="mb-6"
              :color="Number(item.match) < 50 ? 'error' : 'success'"
              height="10"
              :model-value="item.match"
              rounded="pill"
            ></v-progress-linear>
            <v-btn
              class="text-none"
              color="primary"
              variant="text"
              slim
              :href="item.viewUrl"
              target="_blank"
            >
              View Resume<v-icon class="ml-2">mdi-arrow-right</v-icon></v-btn
            >
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <div id="detailed-match-scores1"></div>
    <div v-if="items.length > itemsPerPage" class="d-flex justify-center">
      <v-pagination
        v-model="page"
        :length="Math.ceil(items.length / itemsPerPage)"
        class="mt-4"
        color="white"
        :total-visible="4"
      ></v-pagination>
    </div>
  </div>

  <v-dialog persistent :model-value="overlay" class="align-center justify-center">
    <div class="d-flex justify-center align-self-center loader" align-self="center">
      <v-progress-circular
        :model-value="value"
        indeterminate
        :size="100"
        :width="10"
        color="white"
      >
        {{ value }} %
      </v-progress-circular>
    </div>
  </v-dialog>

  <v-snackbar v-model="showError" :timeout="2000" color="blue-grey" rounded="pill">
    {{ errorMessage }}
  </v-snackbar>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import bannerImg from "@/assets/banner-img.png";
import {
  S3Client,
  ListObjectsCommand,
  DeleteObjectsCommand,
  PutObjectCommand,
  GetObjectCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import mammoth from "mammoth";
import { PDFDocument, rgb } from "pdf-lib";
import axios from "axios";
import { it } from "node:test";
// const items = Array.from({ length: 30 }, (_, index) => index + 1); // Sample data
const items = ref<any>([]);
const jobDescription = ref("");
const selectRange = [
  {
    title: "Show all",
    value: 0,
  },
  {
    title: "Greater than 90%",
    value: 10,
  },
  {
    title: "Greater than 80%",
    value: 20,
  },
  {
    title: "Greater than 60%",
    value: 30,
  },
  {
    title: "Greater than 40%",
    value: 40,
  },
];

const page = ref(1);
const itemsPerPage = 8;
const uploadedFiles = ref<File | any>(null);
const fileInputRef = ref<HTMLInputElement | null>(null);
const overlay = ref(false);
const value = ref(40);
const showError = ref(false);
const errorMessage = ref("");
const search = ref("");
const jDFile = ref<File | any>(null);
const jDFileInputRef = ref<HTMLInputElement | null>(null);

// Computed property to paginate items
const paginatedItems = computed(() => {
  const start = (page.value - 1) * itemsPerPage;
  return transformData(items.value).slice(start, start + itemsPerPage);
});

const convertDocxToPdf = async (file: File) => {
  const arrayBuffer = await file.arrayBuffer();
  const { value: html } = await mammoth.convertToHtml({ arrayBuffer });

  // Create a new PDF document
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage();

  // Draw HTML content onto PDF (basic text)
  const text = html.replace(/<[^>]+>/g, ""); // Simple stripping of HTML tags
  page.drawText(text, {
    x: 50,
    y: page.getHeight() - 50,
    size: 12,
    color: rgb(0, 0, 0),
  });
  // Serialize the PDF document to bytes
  const pdfBytes = await pdfDoc.save();

  // Create a Blob and download the PDF
  const blob = new Blob([pdfBytes], { type: "application/pdf" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${file.name.replace(".docx", ".pdf")}`;
  a.click();
  URL.revokeObjectURL(url);
};

function transformData(data: any) {
  return Object.keys(data)
    .map((key) => ({
      fileName: key,
      match: `${(data[key].score * 100).toFixed(2)}%`,
      viewUrl: data[key].url,
      score: data[key].score, // Keep the score as a number for sorting purposes
    }))
    .sort((a, b) => b.score - a.score) // Sort by score in descending order
    .map((item) => ({
      fileName: item.fileName,
      match: item.match,
      viewUrl: item.viewUrl,
    })); // Remove the score from the final output
}

// Function to handle file upload
const handleFileUpload = (event: any) => {
  const file = event.target.files;
  uploadedFiles.value = [];
  const notSupported = [];
  for (let i = 0; i < file.length; i++) {
    if (file[i].type === "application/pdf") {
      uploadedFiles.value.push(file[i]);
    } else {
      notSupported.push(file[i].name);
    }
  }
  if (notSupported.length > 0) {
    showError.value = true;
    errorMessage.value = `The following files are not supported: ${notSupported.join(
      ","
    )}`;
  }
};
// const handleFileUpload = async (event: any) => {
//   const target = event.target as HTMLInputElement;
//   if (target.files) {
//     const filesArray = Array.from(target.files);
//     uploadedFiles.value = filesArray;

//     // Convert and handle each file
//     for (const file of filesArray) {
//       if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
//         await convertDocxToPdf(file);
//       } else {
//         const file = event.target.files
//         uploadedFiles.value = file
//         console.log(file)
//       }
//     }
//   }
// };

function openFileInput() {
  const fileInput = fileInputRef.value;
  if (fileInput) {
    fileInput.click();
  }
}

function openJdFileInput() {
  const fileInput = jDFileInputRef.value;
  if (fileInput) {
    fileInput.click();
  }
}

const handleJdFileUpload = (event: any) => {
  const file = event.target.files[0];
  jDFile.value = file;
  console.log(file);
};

async function clearBucket(s3Client: any, bucketName: any) {
  // List all objects in the bucket
  const listParams = { Bucket: bucketName };
  const listedObjects = await s3Client.send(new ListObjectsCommand(listParams));
  if (!listedObjects.Contents) return;
  if (listedObjects.Contents.length === 0) return; // No objects to delete

  // Prepare the list of objects to delete
  const deleteParams = {
    Bucket: bucketName,
    Delete: {
      Objects: listedObjects.Contents.map(({ Key }: any) => ({ Key })),
    },
  };

  // Delete all the listed objects
  await s3Client.send(new DeleteObjectsCommand(deleteParams));
  console.log("Bucket cleared!");
}

async function resumeAnalysis() {
  // if (!jobDescription.value || jobDescription.value.length < 10) {
  //   showError.value = true
  //   errorMessage.value = 'Please enter a job description with at least 10 characters'
  //   return
  // }
  if (!jDFile.value) {
    if (!jobDescription.value || jobDescription.value.length < 10) {
      showError.value = true;
      errorMessage.value = "Please enter a job description with at least 10 characters";
      return;
    }
  }
  if (!uploadedFiles.value) {
    showError.value = true;
    errorMessage.value = "Please upload a file";
    return;
  }
  overlay.value = true;
  value.value = 40;

  const s3Client = new S3Client({
    region: process.env.AWS_DEFAULT_REGION,
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    },
  });

  const bucketName = "resume-jd-matcher-resumes";
  const jdBucketName = "resume-jd-matcher-jds";
  // Step 1: Clear the bucket
  await clearBucket(s3Client, bucketName);

  // Step 2: Prepare an array of upload and URL generation promises
  const uploadPromises = Array.from(uploadedFiles.value).map(async (file: any) => {
    const uploadParams = {
      Bucket: bucketName,
      Key: file.name,
      Body: file,
      ContentType: file.type,
    };

    // Upload the file to S3
    await s3Client.send(new PutObjectCommand(uploadParams));
  });

  try {
    await Promise.all(uploadPromises);
    value.value = 60;
  } catch (err) {
    console.error("Error uploading files:", err);
    overlay.value = false;
  }

  try {
    if (jDFile.value) {
      await clearBucket(s3Client, jdBucketName);
      const uploadParams = {
        Bucket: jdBucketName,
        Key: jDFile.value.name,
        Body: jDFile.value,
        ContentType: jDFile.value.type,
      };
      await s3Client.send(new PutObjectCommand(uploadParams));
    }
  } catch (err) {
    console.error("Error uploading file:", err);
  }

  try {
    value.value = 80;
    const response = await axios.post(
      "http://ec2-13-232-186-189.ap-south-1.compute.amazonaws.com/match",
      {
        jobDescription: jobDescription.value,
      }
    );

    if (response.data) {
      value.value = 100;
      items.value = response.data;
      uploadedFiles.value = [];
      jobDescription.value = "";
      jDFile.value = null;
      goTo(`#detailed-match-scores1`);
    }
  } catch (error) {
    console.error(error);
  }

  overlay.value = false;
}

function goTo(selector: any) {
  const element = document.querySelector(selector);
  if (element) {
    const originalId = element.id;
    element.id = "";

    // Temporarily scroll to a different position
    window.scrollTo({ left: 0, behavior: "smooth" });

    // Scroll back to the target element after a short delay
    setTimeout(() => {
      element.id = originalId;
      element.scrollIntoView({ behavior: "smooth", inline: "center" });
    }, 100); // Adjust the timeout as needed
  }
}
</script>

<style>
.custom-tooltip {
  min-width: 170px !important;
  background-color: #f7f7f7 !important;
  color: black;
  margin-left: 15px;
  margin-top: 26px !important;
  border-radius: 8px; /* Apply border-radius here */
  /* padding: 10px 15px; */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  border: 1px solid black;
}

@keyframes moveUpAndDown {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px); /* Moves the image up */
  }
  100% {
    transform: translateY(0); /* Back to the original position */
  }
}

.animated-image {
  animation: moveUpAndDown 3s ease-in-out infinite; /* Adjust duration as needed */
}
</style>
