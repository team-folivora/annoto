<script>
export default {
  data() {
    return {
      input: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    loginUser() {
      if (this.username != "" && this.password != "") {
        // mocked data user
        if (this.input.username == "annoto" && this.input.password == "lol") {
          //TODO backend login logic
          console.log(this.input.username + " " + "authenticated...");
        } else {
          console.log("Username or Password is not correct...");
        }
      } else {
        console.log("Username and Password needs to be set...");
      }
    },
  },
};
</script>

<template>
  <div>
    <input
      v-model="input.username"
      type="text"
      name="Username"
      placeholder="Username"
    /><br />
    <input
      v-model="input.password"
      type="password"
      name="Password"
      placeholder="Password"
    /><br />
    <button type="button" @click="loginUser">Login!</button>
  </div>
</template>
