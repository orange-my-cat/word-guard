<template>
  <section class="h-full">
    <div class="titlename">
      <h1>File Classification</h1>
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
        <p>
          Click on a <span class="font-bold">file name</span> to view its
          results.
        </p>
      </div>
      <div class="box-content h-500 w-300 p-4 columns-auto content mx-auto">
        <div class="icon-container">
          <!--Upload icon source: https://fontawesome.com/icons/folder-open?f=classic&s=regular&pc=%23ff8000-->

          <h1 class="underline underline-offset-8 options">GENUINE FILES</h1>
          <br />
          <div class="filescroller-multi">
            <p id="fileoutput" v-for="file in gen_list" v-bind:key="file">
              <button
                class="bg-green-500 hover:bg-green-400 text-black font-bold py-2 px-4 border-b-4 border-green-700 hover:border-green-500 rounded"
                @click="$router.push('/activity'), fileDetails(file)"
              >
                {{ file }}
              </button>
              <br /><br />
            </p>
          </div>
        </div>
        <div class="icon-container">
          <h1 class="underline underline-offset-8 options">SUSPICIOUS FILES</h1>
          <br />
          <div class="filescroller-multi">
            <p id="fileoutput" v-for="file in sus_list" v-bind:key="file">
              <button
                class="bg-red-500 hover:bg-red-400 text-black font-bold py-2 px-4 border-b-4 border-red-700 hover:border-red-500 rounded"
                @click="$router.push('/activity'), fileDetails(file)"
              >
                {{ file }}
              </button>
              <br /><br />
            </p>
          </div>
        </div>
        <div
          class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4"
          role="alert"
          v-if="hidden"
        >
          <p class="font-bold text-2xl">Genuine Files</p>
          <p class="font-normal">
            The files in this list have presented no indications of cheating.
            The files in this list have presented no indications of cheating.
          </p>
        </div>
        <div
          class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4"
          role="alert"
          v-if="hidden"
        >
          <p class="font-bold text-2xl">Suspicious Files</p>
          <p class="font-normal">
            These files have been flagged for suspicious activity. For an
            in-depth analysis, click on a filename and press the
            <span class="font-bold">Result</span> button. These files have been
            flagged for suspicious activity. For an in-depth analysis, click on
            a filename and press the
            <span class="font-bold">Result</span> button.
          </p>
        </div>
      </div>
      <button @click="$router.push('/')">
        <font-awesome-icon :icon="['fas', 'circle-left']" size="3x" id="info" />
      </button>
    </div>
  </section>
</template>
<script>
// import result from '/results.json';
let results = {};
//
export default {
  name: "HomePage",
  data() {
    return {
      files_list: [],
      flag_list: [],
      sus_list: [],
      gen_list: [],
      hidden: false,
    };
  },
  mounted: function () {
    this.getResults();
    // console.log("getting results: \n");
    // console.log(results);
    // this.suspiciousFiles();
  },
  methods: {
    async getResults() {
      this.setResults(JSON.parse(sessionStorage.getItem("results")));
      console.log(results);
      this.suspiciousFiles();
    },
    setResults: function (res) {
      results = res;
      // console.log(results);
    },
    fileDetails: function (file) {
      this.file = file;
      sessionStorage.setItem("file", this.file);
    },
    suspiciousFiles: function () {
      console.log("checking for suspicious files");
      // console.log(results);
      // eslint-disable-next-line
      for (const file in results) {
        // console.log(file);
        const sus = results[file].suspicious;
        if (sus == false) {
          this.gen_list.push(file);
        }
        if (sus == true) {
          this.sus_list.push(file);
        }
      }
      console.log(this.gen_list);
    },
  },
};
</script>
