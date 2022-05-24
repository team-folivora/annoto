<script lang="ts">
import { defineComponent } from "vue";
import { LoginService as API } from "@/api/services/LoginService";
import { store } from "@/utils/store";

export default defineComponent({
  data() {
    return {
      /**
       * Content of the username filed
       */
      email: "",
      /**
       * Content of the password field
       */
      password: "",
    };
  },

  methods: {
    async loginUser() {
      if (this.email != "" && this.password != "") {
        try {
          let response = await API.login({
            email: this.email,
            password: this.password,
          });
          store.jwt = response.access_token;
          this.$router.push({ name: "Home" });
        } catch {
          this.$toast?.danger("E-Mail or Password is not correct...");
        }
      } else {
        this.$toast?.warning("E-Mail and Password need to be set...");
      }
    },
  },
});
</script>

<template>
  <div id="login-view" class="_margin-x:auto _margin-top:8">
    <i-input v-model="email" type="email" name="email" placeholder="E-Mail" />
    <br />
    <i-input
      v-model="password"
      type="password"
      name="password"
      placeholder="Password"
      @keyup.enter="loginUser"
    />
    <br />
    <i-button id="submit" type="button" @click="loginUser">Login!</i-button>
  </div>
</template>

<style scoped>
div {
  max-width: 300px;
}
</style>
