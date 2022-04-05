import { createApp } from "vue";
import App from "./App.vue";

import { Inkline, components } from "@inkline/inkline";
import "@inkline/inkline/inkline.scss";

import "./assets/base.scss";

import { OpenAPI } from "./api/core/OpenAPI"
OpenAPI.BASE = import.meta.env.VITE_API_URL?.toString().replace(/\/$/, "") || "";

const app = createApp(App);

app.use(Inkline, {
  components,
});

app.mount("#app");
