import { createApp } from "vue";
import App from "@/App.vue";

import { Inkline, components } from "@inkline/inkline";
import "@inkline/inkline/inkline.scss";

import VueCookies from "vue-cookies";
import { createRouter, createWebHashHistory } from "vue-router";

import "@/assets/base.scss";

import { OpenAPI } from "@/api/core/OpenAPI";
import Toaster from "@/plugins/toaster";
import LoginView from "./components/LoginView.vue";
import TasksOverView from "./components/TasksOverView.vue";
import TaskView from "./components/TaskView.vue";
import RedirectView from "./components/RedirectView.vue";
import { store } from "@/utils/store";

OpenAPI.BASE =
  import.meta.env.VITE_API_URL?.toString().replace(/\/$/, "") || "";

const app = createApp(App);

app.use(Inkline, {
  components,
});

app.use(Toaster);

app.use(VueCookies, { expire: "1d" });

const routes = [
  { path: "/", component: RedirectView },
  {
    path: "/login",
    component: LoginView,
    beforeEnter: () => {
      return store.isLoggedIn ? "/tasks" : true;
    },
  },
  {
    path: "/tasks",
    component: TasksOverView,
    beforeEnter: () => {
      return store.isLoggedIn ? true : "/login";
    },
  },
  {
    path: "/tasks/:taskid",
    component: TaskView,
    beforeEnter: () => {
      return store.isLoggedIn ? true : "/login";
    },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

app.use(router);

app.mount("#app");
