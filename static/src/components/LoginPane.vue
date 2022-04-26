<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
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
        // mocked data user
        if (this.username == "annoto" && this.password == "lol") {
          //TODO backend login logic
          console.log(this.username + " " + "authenticated...");
          this.$emit("login");
        } else {
          console.log("Username or Password is not correct...");
        }
      } else {
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
      name="Username"
      placeholder="Username"
    />
    <br />
    <input
      v-model="password"
      type="password"
      name="Password"
      placeholder="Password"
    />
    <br />
    <button type="button" @click="loginUser">Login!</button>
  </div>
</template>
