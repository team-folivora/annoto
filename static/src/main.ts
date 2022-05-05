import { createApp } from "vue";
import App from "@/App.vue";

import { Inkline, components } from "@inkline/inkline";
import "@inkline/inkline/inkline.scss";

import VueCookies from "vue-cookies";

import "@/assets/base.scss";

import { OpenAPI } from "@/api/core/OpenAPI";
import Toaster from "@/plugins/toaster";

OpenAPI.BASE =
  import.meta.env.VITE_API_URL?.toString().replace(/\/$/, "") || "";

const app = createApp(App);

app.use(Inkline, {
  components,
});

app.use(Toaster);

app.use(VueCookies, { expire: "1d" });

app.mount("#app");
