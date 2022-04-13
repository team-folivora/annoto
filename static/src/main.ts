import { createApp } from "vue";
import App from "./App.vue";

import { Inkline, components } from "@inkline/inkline";
import "@inkline/inkline/inkline.scss";

import "./assets/base.scss";

import { OpenAPI } from "./api/core/OpenAPI";
import Toaster from "./plugins/toaster";

OpenAPI.BASE =
  import.meta.env.VITE_API_URL?.toString().replace(/\/$/, "") || "";

const app = createApp(App, {
  taskId: "ecg-qrs-classification-physiodb",
  competency: "Prof. Dr. Med.",
  user: "AnnotoUser#1337",
});

app.use(Inkline, {
  components,
});

app.use(Toaster);

app.mount("#app");
