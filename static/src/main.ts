import { OpenAPI } from "@/api/core/OpenAPI";
import App from "@/App.vue";
import Toaster from "@/plugins/toaster";
import "@/utils/theme";
import ElementPlus from "element-plus";
import "element-plus/theme-chalk/src/message.scss";
import { createApp } from "vue";
import VueCookies from "vue-cookies";

OpenAPI.BASE =
  import.meta.env.VITE_API_URL?.toString().replace(/\/$/, "") || "";

const app = createApp(App);

app.use(ElementPlus);

app.use(Toaster);

app.use(VueCookies, { expire: "1d" });

app.mount("#app");
