import { type App, reactive, type Plugin } from "vue";
import { OpenAPI } from "@/api";
import type { VueCookies } from "vue-cookies";
import type { StoreApi } from "@/plugins/types";

export const store: StoreApi = reactive({
  _jwt: undefined as string | undefined,

  $cookies: undefined as VueCookies | undefined,

  isLoggedIn: false as boolean,

  initialize(cookies: VueCookies) {
    this.$cookies = cookies;
    this.jwt = cookies.get("jwt");
  },

  get jwt() {
    return this._jwt;
  },

  set jwt(newJWT) {
    if (newJWT) {
      this._jwt = newJWT;
      this.isLoggedIn = true;
      OpenAPI.TOKEN = newJWT;
      this.$cookies?.set("jwt", newJWT);
    } else {
      this.removeJwt();
    }
  },

  removeJwt() {
    this._jwt = undefined;
    this.isLoggedIn = false;
    OpenAPI.TOKEN = undefined;
    this.$cookies?.remove("jwt");
  },
});

function createStore(app: App): StoreApi {
  if (!app.config.globalProperties.$cookies) {
    throw new Error("VueCookies is not installed");
  }
  store.initialize(app.config.globalProperties.$cookies);
  return store;
}

export const Store: Plugin = {
  install(app: App) {
    app.config.globalProperties.$store = createStore(app);
  },
};
