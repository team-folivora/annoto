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
      username: "",
      /**
       * Content of the password field
       */
      password: "",
    };
  },

  methods: {
    async loginUser() {
      if (this.username != "" && this.password != "") {
        try {
          await API.login({
            username: this.username,
            password: this.password,
          });
          console.log(this.username + " " + "authenticated...");
          this.$emit("login");
        } catch (ex) {
          console.log("Username or Password is not correct...");
          this.$toast?.danger("Username or Password is not correct...");
        }
      } else {
        this.$toast?.warning("Username and Password needs to be set...");
        console.log("Username and Password needs to be set...");
      }
    },
  },
});
</script>

<template>
  <div>
    <input
      v-model="username"
      type="text"
      name="username"
      placeholder="Username"
    />
    <br />
    <input
      v-model="password"
      type="password"
      name="password"
      placeholder="Password"
    />
    <br />
    <button type="button" @click="loginUser" id="submit">Login!</button>
  </div>
</template>
