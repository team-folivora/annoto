import { reactive } from "vue";
import { OpenAPI } from "@/api";
import type { VueCookies } from "vue-cookies";

export const store = reactive({
  _jwt: undefined as string | undefined,

  $cookies: undefined as VueCookies | undefined,

  isLoggedIn: false,

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
