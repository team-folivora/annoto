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
    loginUser() {
      if (this.username != "" && this.password != "") {
        API.login({
          username: this.username,
          password: this.password,
        })
          .then((() => this.$emit("login")).bind(this))
          .catch(
            (() =>
              this.$toast?.danger(
                "Username or Password is not correct..."
              )).bind(this)
          );
      } else {
        this.$toast?.warning("Username and Password needs to be set...");
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
    <button id="submit" type="button" @click="loginUser">Login!</button>
  </div>
</template>
