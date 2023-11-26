<script>
import chartComp from "../components/ChartComp.vue";
import doughnutChart from "../components/doughnutChart.vue";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

const chartColor = (cheater) => {
  if (cheater == false) {
    return "green";
  }
  if (cheater) {
    return "#D21404";
  }
};

export default {
  name: "HomePage",
  components: {
    chartComp,
    doughnutChart,
  },
  data() {
    const resultData = {
      rsidR: {},
      rsidRDefault: {},
      rsidP: {},
      rsidSect: {},
      filename: "",
      words: 0,
      authors: [],
      version: 0,
      tval: 0,
      suspicious: "",
      created: "",
      last_modified: "",
      edit_time: 0,
    };
    return {
      resultData: resultData,
      file: "",
      hidden: false,
      textColor: chartColor(resultData.suspicious),
      screenshots: [],
      chartData: {
        labels: Object.keys(resultData.rsidR),
        datasets: [
          {
            backgroundColor: chartColor(resultData.suspicious),
            data: Object.values(resultData.rsidR),
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "70%",
        plugins: {
          legend: {
            display: false,
          },
        },
      },
      chartPlugins: [
        {
          id: "text",
          beforeDraw: function (chart) {
            const width = chart.width;
            const height = chart.height;
            const ctx = chart.ctx;

            ctx.restore();
            const fontSize = (height / 190).toFixed(2);
            ctx.font = fontSize + "em sans-serif";
            ctx.fillStyle = chartColor(resultData.suspicious);
            ctx.textBaseline = "middle";
            const text = Object.keys(resultData.rsidR).length + ` Unique RSID`;
            const textX = Math.round((width - ctx.measureText(text).width) / 2);
            const textY = height / 2;

            ctx.fillText(text, textX, textY);
            ctx.save();
          },
        },
      ],
    };
  },
  mounted: function () {
    this.getFileData();
  },
  methods: {
    getFileData() {
      const selectedFile = sessionStorage.getItem("file");
      const result = JSON.parse(sessionStorage.getItem("results"));
      this.file = Object.keys(result).length;
      this.resultData.filename = selectedFile;
      this.resultData.tval = result[selectedFile].probability;
      this.resultData.rsidR = result[selectedFile].rsidR;
      this.resultData.authors = result[selectedFile].authors[0][0];
      this.resultData.rsidP = result[selectedFile].rsidP;
      this.resultData.rsidRDefault = result[selectedFile].rsidRDefault;
      if (result[selectedFile].rsidSect != null) {
        this.resultData.rsidSect = result[selectedFile].rsidSect;
      }
      this.resultData.words = result[selectedFile].words;
      this.resultData.suspicious = result[selectedFile].suspicious;
      this.resultData.edit_time = result[selectedFile].edit_time;
      this.resultData.version = result[selectedFile].version;
      this.resultData.created = result[selectedFile].created;
      this.resultData.last_modified = result[selectedFile].last_modified;
      this.colours(this.resultData.suspicious);
      console.log("RSID VALS", Object.keys(this.resultData.rsidR));
      console.log("THese are the authors", this.resultData.authors);
      console.log("Is it suspicious?", this.resultData.suspicious);
      console.log(
        "This is the file from the get request",
        result[selectedFile].rsidSect
      );
    },
    colours(sus) {
      if (sus) {
        return "#D21404";
      } else {
        return "green";
      }
    },
    chartData_Organiser() {
      const chartData = {
        labels: Object.keys(this.resultData.rsidR),
        datasets: [
          {
            label: this.resultData.authors,
            data: Object.values(this.resultData.rsidR),
            borderColor: "#e0e5fd",
            backgroundColor: this.colours(this.resultData.suspicious),
          },
        ],
      };
      return chartData;
    },
    exportResult() {
      if (this.hidden == true) {
        console.log("Printing");
        this.takeScreenshot(() => {
          this.generatePDF();
        });
      } else {
        alert("Please click the information button");
      }
    },
    takeScreenshot(callback) {
      html2canvas(document.body).then((canvas) => {
        const imgData = canvas.toDataURL("image/png");
        this.screenshots.push(imgData);
        if (this.screenshots.length === 1) {
          callback();
        }
      });
    },
    generatePDF() {
      const pdf = new jsPDF();
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const imageWidth = pageWidth - 20;
      const imageHeight = (imageWidth / pageWidth) * pageHeight;
      pdf.addImage(
        this.screenshots[0],
        "PNG",
        10,
        10,
        imageWidth,
        imageHeight,
        "",
        "FAST"
      );
      pdf.save(`screenshot_${Date.now()}.pdf`);
    },
    reloadPage() {
      const url = new URL("/", window.location.origin);
      window.location.href = url.toString();
    },
  },
  computed: {
    ratio() {
      const numRsid = Object.keys(this.resultData.rsidR).length;
      return Math.round(this.resultData.words / numRsid);
    },
  },
};
</script>

<template>
  <section class="flex flex-col items-center justify-center">
    <div class="max-w-[80%] container">
      <div class="flex m-3 justify-end w-full">
        <font-awesome-icon
          :icon="['fas', 'circle-info']"
          class="text-[#E39623] w-16 h-16"
          id="info"
          @click="hidden = !hidden"
        />
        <div
          v-if="resultData.suspicious"
          class="w-full justify-center flex items-center"
        >
          <font-awesome-icon
            :icon="['fas', 'circle-exclamation']"
            class="w-16 h-16 m-5 text-[#B80C0C]"
          />
          <p class="text-3xl font-bold">THIS FILE HAS BEEN FLAGGED AS</p>
          <p class="text-[#B80C0C] ml-3 text-3xl font-bold">SUSPICIOUS</p>
        </div>

        <div v-else class="w-full justify-center flex items-center">
          <font-awesome-icon
            :icon="['fas', 'face-smile']"
            class="w-16 h-16 m-5 text-[#32791A]"
          />
          <p class="text-3xl font-bold">THIS FILE HAS</p>
          <p class="text-[#32791A] ml-3 text-3xl font-bold">NOT</p>
          <p class="ml-3 text-3xl font-bold">BEEN FLAGGED AS SUSPICIOUS</p>
        </div>

        <font-awesome-icon
          :icon="['fas', 'house']"
          class="text-[#E39623] w-16 h-16"
          id="info"
          @click="$router.push('/')"
        />
      </div>
      <p class="text-xl text-center">
        <span class="font-bold">Selected File: </span>
        <span class="font-skinny">{{ resultData.filename }}</span>
      </p>
      <br />
      <div
        class="bg-orange-100 border-l-4 border-orange-500 text-orange-700 p-4 w-full mb-5"
        role="alert"
        v-if="hidden"
      >
        <p class="font-bold">Number of rsidR</p>
        <p>
          This represents the count of unique rsidR instances found in the
          document. Each rsidR indicates a saved revision. While the document
          contains various types of rsids, for the context of our analysis, we
          primarily focus on rsidR for categorizing instances of cheating.
        </p>
        <br />
        <p>
          The doughnut pie chart visually represents the distribution of unique
          rsid values by their respective frequencies of appearance. When you
          hover over each segment, you can view both the specific unique rsidR
          value and its corresponding frequency.
        </p>
        <br />
        <p class="font-bold">Types of Rsid</p>
        <li>rsidR: Represents Run-Level Revisions</li>
        <li>rsidRDefault: Represents Default Run-Level Revisions</li>
        <li>rsidP: Represents Paragraph-Level Revisions</li>
        <li>rsidSect: Represents Section-Level Revisions</li>
        <br />
        <p class="font-bold">Number of Words</p>
        <p>This corresponds to the total word count in the document.</p>
        <br />
        <p class="font-bold">Ratio word-to-rsid</p>
        <p>
          This is the ratio of the total number of words in the document divided
          by the number of rsidR instances. It provides insight into the
          revision density.
        </p>
        <br />
        <p class="font-bold">Number of Authors</p>
        <p>
          Indicates the number of distinct authors identified in the document.
          Typically, genuine submissions have a single author for individual
          submissions.
        </p>
        <br />
        <p class="font-bold">Probability</p>
        <p>
          This is the probability that the file is cheating, calculated using a
          logistic regression model based on metadata extracted from the
          document.
        </p>
        <br />
        <p class="font-bold">File information</p>
        <p>Versions:</p>
        <li>v.12 is Office 2007</li>
        <li>v.14 is Office 2010</li>
        <li>v.15 is Office 2013</li>
        <li>v.16 is Office 2016</li>
        <br />
        <p>Editing Time:</p>
        <p>
          Indicates the total minutes the document has been edited, extracted
          from document properties in MS Word. This can reflect the level of
          effort put into editing or revising the document. A low editing time
          compare to words can indicate to suspicions of cheating.
        </p>
        <br />
        <p>Creation Date:</p>
        <p>Specifies the date on which the document was originally created.</p>
        <br />
        <p>Last Edit:</p>
        <p>
          Shows the date on which the document was last edited, providing
          insights into its recent updates or modifications.
        </p>
        <br />
        <p class="font-bold text-[#121445]">Indications of cheating:</p>
        <p class="text-[#121445]">
          All the relevant factors are incorporated into a logic model, which is
          used to analyze and compare these factors within a distribution. A
          probability value is then calculated to assess the likelihood that the
          document is fraudulent. It's important to note that a 50% significance
          level is employed in this model, setting the threshold for making
          determinations regarding the document's authenticity.
        </p>
      </div>
      <div class="grid grid-cols-3 gap-5 w-full max-h-[80%] resize-x">
        <!-- first column -->
        <div class="grid grid-rows-2 gap-5 h-full">
          <chartComp title="Number of rsidR" class="h-full">
            <doughnutChart
              :chartOptions="chartOptions"
              :chartData="chartData_Organiser()"
              :chartPlugins="chartPlugins"
            />
          </chartComp>
          <chartComp title="Types of Rsid" class="h-full">
            <h2 class="ml-5 text-xl font-bold">rsidP</h2>
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="ml-5 text-xl font-bold"
            >
              {{ Object.keys(resultData.rsidP).length }}
            </h2>
            <hr class="w-auto m-5 border-black" />
            <h2 class="ml-5 text-xl font-bold">rsidRDefault</h2>
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="ml-5 text-xl font-bold"
            >
              {{ Object.keys(resultData.rsidRDefault).length }}
            </h2>
            <hr class="w-auto m-5 border-black" />
            <h2 class="ml-5 text-xl font-bold">rsidSect</h2>
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="ml-5 text-xl font-bold"
            >
              {{ Object.keys(resultData.rsidSect).length }}
            </h2></chartComp
          >
        </div>
        <!-- second column -->
        <div class="grid grid-rows-[2fr,2fr,4fr] gap-5 h-full">
          <chartComp title="Number of Words" class="h-full">
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="m-5 text-6xl font-bold"
            >
              {{ resultData.words }}
            </h2></chartComp
          >
          <chartComp title="Ratio word-to-rsid" class="h-full">
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="m-5 text-6xl font-bold"
            >
              {{ ratio }}
            </h2></chartComp
          >
          <chartComp title="Number of Author(s)" class="h-full">
            <span
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="m-5 text-6xl font-bold"
              >{{ resultData.authors.length }}</span
            >
            <hr class="w-auto m-5 border-black" />
            <ul class="text-left m-5">
              <li v-for="author in resultData.authors" :key="author">
                {{ author }}
              </li>
            </ul></chartComp
          >
        </div>
        <!-- third column -->
        <div class="grid grid-rows-[2fr,5fr,1fr] gap-5 h-full">
          <chartComp
            v-if="resultData.suspicious"
            title="Probability"
            class="h-full bg-[#FFCBCB]"
            ><h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="m-5 text-6xl font-bold"
            >
              {{ resultData.tval }}
            </h2>
          </chartComp>
          <chartComp v-else title="Probability" class="h-full bg-[#ccffdb]"
            ><h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="m-5 text-6xl font-bold"
            >
              {{ resultData.tval }}
            </h2>
          </chartComp>
          <chartComp title="File Information" class="h-full"
            ><div
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="m-5 text-xl font-bold text-center"
            >
              <span> {{ resultData.version }} </span>
            </div>
            <hr class="w-auto m-5 border-black" />
            <h2 class="ml-5 text-xl font-bold">Total Editing Time</h2>
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="ml-5 text-xl font-bold"
            >
              {{ resultData.edit_time }} minutes
            </h2>
            <hr class="w-auto m-5 border-black" />
            <h2 class="ml-5 text-xl font-bold">Creation Date</h2>
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="ml-5 text-xl font-bold"
            >
              {{ resultData.created }}
            </h2>
            <hr class="w-auto m-5 border-black" />
            <h2 class="ml-5 text-xl font-bold">Last Edit</h2>
            <h2
              :style="{
                color: colours(resultData.suspicious),
              }"
              class="ml-5 text-xl font-bold"
            >
              {{ resultData.last_modified }}
            </h2>
          </chartComp>
          <div class="grid grid-cols-3 gap-5 h-full">
            <v-btn
              @click="exportResult()"
              class="bg-white bg-opacity-75 rounded-3xl flex col-span-2 items-center hover:bg-[#121445] hover:text-white"
            >
              <font-awesome-icon
                :icon="['fas', 'download']"
                class="h-8 w-8 text-[#E39623] m-3"
              />
              <p class="font-bold text-center">Download Result</p>
            </v-btn>
            <v-btn
              class="bg-white bg-opacity-75 rounded-3xl flex justify-center items-center hover:bg-[#121445]"
              @click="$router.push('/multiDisplay')"
              v-if="file > 1"
            >
              <font-awesome-icon
                :icon="['fas', 'arrow-rotate-left']"
                class="h-8 w-8 text-[#E39623] m-3"
              />
            </v-btn>
            <v-btn
              class="bg-white bg-opacity-75 rounded-3xl flex justify-center items-center hover:bg-[#121445]"
              @click="$router.push('/')"
              v-if="file == 1"
            >
              <font-awesome-icon
                :icon="['fas', 'arrow-rotate-left']"
                class="h-8 w-8 text-[#E39623] m-3"
              />
            </v-btn>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
