import { createApp } from "vue";
import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import App from "./App.vue";
import Home from "./views/HomePage.vue";
import Activity from "./views/ActivityPage.vue";
import MultipleFileDisplay from "./views/MultipleFileDisplayPage.vue";
import "./style.css";

const routes = [
  { path: "/", component: Home },
  { path: "/activity", component: Activity },
  { path: "/multiDisplay", component: MultipleFileDisplay },
];

const router = createRouter({
  history: process.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(),
  routes: routes,
});

/* Sourced from https://fontawesome.com/docs/web/use-with/vue/add-icons tutorial to make font-awesome fonts work with Vue */
/* import the fontawesome core */
import { library } from "@fortawesome/fontawesome-svg-core";

/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

/* import specific icons */
import { fas } from "@fortawesome/free-solid-svg-icons";

/* add icons to the library */
library.add(fas);

createApp(App)
  .component("font-awesome-icon", FontAwesomeIcon)
  .use(router)
  .mount("#app");
