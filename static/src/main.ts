import { createApp } from "vue";
import App from "@/App.vue";

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// import "element-plus/theme-chalk/src/message.scss"

import VueCookies from "vue-cookies";

// import "@/assets/base.scss";

import { OpenAPI } from "@/api/core/OpenAPI";
import Toaster from "@/plugins/toaster";

OpenAPI.BASE =
  import.meta.env.VITE_API_URL?.toString().replace(/\/$/, "") || "";

const app = createApp(App);

app.use(ElementPlus)

app.use(Toaster);

app.use(VueCookies, { expire: "1d" });

app.mount("#app");
