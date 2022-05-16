<script lang="ts">
import { defineComponent } from "vue";
import TaskOverView from "./components/TaskOverView.vue";
import LoginView from "./components/LoginView.vue";
import { OpenAPI, PingService } from "@/api";
import TaskView from "./components/TaskView.vue";
import type { Task } from "@/api/models/Task";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    TaskOverView,
    LoginView,
    TaskView,
  },
  data() {
    return {
      page: "login",
      task: undefined as Task | undefined,
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
        this.page = "tasks";
        this.loggedIn = true;
      } catch (_) {
        this.logout();
      }
    },

    annotate(task: Task) {
      this.task = task;
      this.page = "task";
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
      <i-row center middle>
        <i-column md="3"></i-column>
        <i-column md="6"><h1 class="_text-align:center">Annoto</h1></i-column>
        <i-column md="3">
          <i-button v-if="loggedIn" id="logout-button" @click="logout">
            Logout
          </i-button>
        </i-column>
      </i-row>
    </i-layout-header>
    <i-layout-content>
      <LoginView
        v-if="page == 'login'"
        id="login-view"
        @login="login"
      ></LoginView>
      <TaskOverView
        v-else-if="page == 'tasks'"
        id="tasks-overview"
        @annotate="annotate"
      ></TaskOverView>
      <TaskView
        v-else-if="page == 'task' && task"
        id="task-view"
        :task="task"
        competency="Prof. Dr. med."
      ></TaskView>
      <div v-else>Invalid Page</div>
    </i-layout-content>
  </i-layout>
</template>
