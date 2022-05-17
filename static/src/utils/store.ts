import { reactive } from "vue";
import { OpenAPI } from "@/api";

export const store = reactive({
  _jwt: undefined as string | undefined,

  $cookies: undefined as any | undefined,

  isLoggedIn: false,

  initialize(cookies: any) {
    this.$cookies = cookies;
    this.jwt = cookies.get("jwt");
  },

  get jwt() {
    return this._jwt;
  },

  set jwt(newJWT) {
    this._jwt = newJWT;
    this.isLoggedIn = !!newJWT;
    OpenAPI.TOKEN = newJWT;
    if (newJWT) {
      this.$cookies.set("jwt", newJWT);
    } else {
      this.$cookies.remove("jwt");
    }
  },
});
