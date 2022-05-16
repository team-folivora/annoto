<script lang="ts">
import { defineComponent } from "vue";
import TaskOverView from "./components/TaskOverView.vue";
import LoginView from "./components/LoginView.vue";
import { OpenAPI, PingService } from "@/api";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    TaskOverView,
    LoginView,
  },
  data() {
    return {
      page: "login",
    };
  },

  async mounted() {
    const jwt = this.$cookies.get("jwt");
    if (jwt) {
      this.login(jwt);
    }
  },

  methods: {
    async login(token: string) {
      try {
        OpenAPI.TOKEN = token;
        await PingService.ping();
        this.page = "task";
      } catch (_) {
        OpenAPI.TOKEN = undefined;
        this.$cookies.remove("jwt");
      }
    },
  },
});
</script>

<template>
  <i-layout>
    <i-layout-header>
      <h1 class="_text-align:center">Annoto</h1>
    </i-layout-header>
    <i-layout-content>
      <LoginView
        v-if="page == 'login'"
        id="login-view"
        @login="login"
      ></LoginView>
      <TaskOverView v-else id="task-view"></TaskOverView>
    </i-layout-content>
  </i-layout>
</template>
