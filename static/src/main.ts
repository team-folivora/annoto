import { createApp } from "vue";
import App from "@/App.vue";

import { Inkline, components } from "@inkline/inkline";
import "@inkline/inkline/inkline.scss";

import VueCookies from "vue-cookies";
import {
  createRouter,
  createWebHistory,
  type RouteLocationRaw,
} from "vue-router";

import "@/assets/base.scss";

import { OpenAPI } from "@/api/core/OpenAPI";
import Toaster from "@/plugins/toaster";
import LoginView from "./components/LoginView.vue";
import TasksOverView from "./components/TasksOverView.vue";
import TaskView from "./components/TaskView.vue";
import { store, Store } from "@/plugins/store";

OpenAPI.BASE =
  import.meta.env.VITE_API_URL?.toString().replace(/\/$/, "") || "";

const app = createApp(App);

app.use(Inkline, {
  components,
});

app.use(Toaster);

app.use(VueCookies, { expire: "1d" });

app.use(Store);

function checkLogin(): boolean | RouteLocationRaw {
  return store.isLoggedIn ? true : { name: "Login" };
}

const routes = [
  {
    path: "/",
    name: "Home",
    redirect: { name: "Tasks" },
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
    beforeEnter: () => {
      return store.isLoggedIn ? { name: "Home" } : true;
    },
  },
  {
    path: "/tasks",
    name: "Tasks",
    component: TasksOverView,
    beforeEnter: checkLogin,
  },
  {
    path: "/tasks/:taskId",
    name: "Task",
    component: TaskView,
    beforeEnter: checkLogin,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

app.use(router);

app.mount("#app");
