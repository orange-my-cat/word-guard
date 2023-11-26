<script>
import { Doughnut } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

export default {
  name: "DoughnutChart",
  components: { Doughnut },
  props: {
    chartData: Object,
    chartOptions: Object,
    chartPlugins: Array,
  },
};
</script>
<template>
  <div>
    <Doughnut
      id="my-chart-id"
      :options="chartOptions"
      :data="chartData"
      :plugins="chartPlugins"
    />
  </div>
</template>
