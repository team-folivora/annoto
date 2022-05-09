<script lang="ts">
import { defineComponent } from "vue";
import { LoginService as API } from "@/api/services/LoginService";
import { ElMessage } from "element-plus";

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
          let response = await API.login({
            email: this.email,
            password: this.password,
          });
          const jwt = response.access_token;
          this.$cookies.set("jwt", jwt);
          this.$emit("login", jwt);
        } catch {
          ElMessage({
            message: "E-Mail or Password is not correct...",
            type: "error",
            showClose: true,
          });
        }
      } else {
        ElMessage({
          message: "E-Mail and Password need to be set...",
          type: "warning",
          showClose: true,
        });
      }
    },
  },
});
</script>

<template>
  <el-row justify="center">
    <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
      <el-space direction="vertical" :fill="true" style="width: 100%">
        <el-input
          v-model="email"
          type="email"
          name="email"
          placeholder="E-Mail"
        />
        <el-input
          v-model="password"
          type="password"
          name="password"
          placeholder="Password"
          @keyup.enter="loginUser"
        />
        <el-button id="submit" @click="loginUser">Login!</el-button>
      </el-space>
    </el-col>
  </el-row>
</template>
