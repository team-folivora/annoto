<script lang="ts">
import { defineComponent } from "vue";
import TaskView from "./components/TaskView.vue";
import LoginView from "./components/LoginView.vue";
import { OpenAPI, PingService } from "@/api";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    TaskView,
    LoginView,
  },
  data() {
    return {
      page: "login",
      loggedIn: false,
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
        this.loggedIn = true;
      } catch (_) {
        this.logout();
      }
    },
    logout() {
      OpenAPI.TOKEN = undefined;
      this.$cookies.remove("jwt");
      this.page = "login";
      this.loggedIn = false;
    },
  },
});
</script>

<template>
  <i-layout>
    <i-layout-header>
      <h1 class="_text-align:center">Annoto</h1>
      <i-button v-if="loggedIn" id="logout-button" @click="logout">
        Logout
      </i-button>
    </i-layout-header>
    <i-layout-content>
      <LoginView
        v-if="page == 'login'"
        id="login-view"
        @login="login"
      ></LoginView>
      <TaskView
        v-else
        id="task-view"
        task-id="ecg-qrs-classification-physiodb"
        competency="Prof. Dr. Med."
      ></TaskView>
    </i-layout-content>
  </i-layout>
</template>
