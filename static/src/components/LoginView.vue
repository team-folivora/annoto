<script lang="ts">
import { defineComponent } from "vue";
import { LoginService as API } from "@/api/services/LoginService";

export default defineComponent({
  emits: ["login"],

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
          await API.login({
            email: this.email,
            password: this.password,
          });
          this.$emit("login");
        } catch {
          this.$toast?.danger("Username or Password is not correct...");
        }
      } else {
        this.$toast?.warning("Username and Password need to be set...");
      }
    },
  },
});
</script>

<template>
  <div class="_margin-x:auto _margin-top:8">
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

<style>
div {
  max-width: 300px;
}
</style>
