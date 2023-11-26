<template>
  <section class="h-full">
    <div class="titlename">
      <h1>Cheating Detection</h1>
    </div>

    <div class="max-w-[80%] container">
      <!--https://stackoverflow.com/questions/48929139/hide-div-onclick-in-vue-js reference to hide info-->

      <font-awesome-icon
        :icon="['fas', 'circle-info']"
        size="3x"
        id="info"
        v-on:click="hidden = !hidden"
      /><br /><br />
      <div
        class="bg-orange-100 border-l-4 border-orange-500 text-orange-700 p-4"
        role="alert"
        v-if="hidden"
      >
        <p class="font-bold">File Upload</p>
        <p>
          Click on the orange folder to browse your files
          <span class="font-bold">or</span> drag your files onto the orange
          folder to upload.
        </p>
      </div>
      <div class="box-content h-500 w-300 p-4 columns-auto content mx-auto">
        <div class="icon-container">
          <!--Upload icon source: https://fontawesome.com/icons/folder-open?f=classic&s=regular&pc=%23ff8000-->
          <div class="icon-images">
            <h1 class="options">Browse/Drag and Drop Files</h1>
            <br />
            <label for="file">
              <font-awesome-icon
                class="file_icon"
                icon="folder-open"
                size="10x"
              />
            </label>
            <br /><br />
            <p>
              .DOCX is the
              <span style="text-decoration: underline">only</span> file format
              accepted
            </p>
            <br />
            <div
              class="bg-orange-100 border-l-4 border-orange-500 text-orange-700 p-4"
              role="alert"
            >
              <p>Folders can not be uploaded.</p>
              <p class="underline text-xl">Max of 50 files</p>
            </div>
            <label style="display: block; text-align: center" />
            <form role="form" method="POST" enctype="multipart/form-data">
              <input
                id="file"
                type="file"
                accept=".docx"
                @change="filesSelected"
                ref="file"
                multiple
              /><br /><br />
            </form>
          </div>
        </div>
        <div class="icon-container">
          <h1 class="underline underline-offset-8 options">Chosen Files</h1>
          <br />
          <div class="filescroller">
            <div class="filescroller">
              <p id="fileoutput" v-for="files in file" v-bind:key="files">
                <font-awesome-icon
                  :icon="['fas', 'check']"
                  size="xs"
                  style="color: #008000"
                />
                {{ files.name }}<br /><br />
              </p>
            </div>
          </div>
        </div>

        <div
          class="bg-red-100 border-l-4 border-red-500 text-orange-700 p-4 text-center"
          role="alert"
          v-if="file.length > 50"
        >
          <p class="font-bold text-2xl text-red-700">
            Maximum File Limit Reached
          </p>
          <p>
            Too many files have been selected. Please try again by reselecting
            your files.
          </p>
        </div>
        <div class="flex items-center justify-center col-span-2">
          <button
            class="h-20 w-40 bg-orange-500 hover:bg-amber-400 text-2xl text-white font-bold m-5 border-b-4 border-orange-700 hover:border-amber-500 rounded-full button"
            id="process"
            @click="uploadFiles(), fileDetails(file)"
            v-if="file.length == 1 && file.length <= 50"
          >
            Process
          </button>
          <button
            class="h-20 w-40 bg-orange-500 hover:bg-amber-400 text-2xl text-white font-bold m-5 border-b-4 border-orange-700 hover:border-amber-500 rounded-full button"
            id="process"
            @click="uploadFiles()"
            v-if="file.length > 1 && file.length <= 50"
          >
            Process
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
export default {
  name: "HomePage",
  data() {
    return {
      file: "",
      hidden: false,
    };
  },
  methods: {
    filesSelected() {
      this.file = this.$refs.file.files;
    },
    fileDetails: function () {
      sessionStorage.setItem("file", this.file[0].name);
    },
    async uploadFiles() {
      this.file = this.$refs.file.files;
      const files = new FormData();
      console.log(this.file, "This . files");
      // eslint-disable-next-line
      for (const currfile in this.file) {
        files.append("files", this.file[currfile]);
        console.log(files);
      }
      console.log("Files", files);
      await axios
        .post("http://localhost:8000/uploads/", files, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log(response.data);
          // alert("File(s) Uploaded Successfully!");
        })
        .catch((response) => {
          console.log("Failed to send file(s) to the server", response.data);
        });
      const result = await axios.get("http://localhost:8000/process/");
      sessionStorage.setItem("results", JSON.stringify(result.data));
      console.log(result);
      if (this.file.length == 1) {
        this.$router.push("/activity");
      } else {
        this.$router.push("/multiDisplay");
      }
    },
  },
};
</script>
