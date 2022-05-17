<script lang="ts">
import { defineComponent } from "vue";
import TasksOverView from "./components/TasksOverView.vue";
import LoginView from "./components/LoginView.vue";
import TaskView from "./components/TaskView.vue";
import type { Task } from "@/api/models/Task";
import { OpenAPI, PingService } from "@/api";
import { isLoggedIn } from "@/utils/store";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    TasksOverView,
    LoginView,
    TaskView,
  },

  data() {
    return {
      page: "login",
      task: undefined as Task | undefined,
      ready: false,
      isLoggedIn,
    };
  },

  async mounted() {
    const jwt = this.$cookies.get("jwt");
    if (jwt) {
      try {
        OpenAPI.TOKEN = jwt;
        await PingService.ping();
      } catch (_) {
        OpenAPI.TOKEN = undefined;
        this.$cookies.remove("jwt");
      }
    } else {
      this.$cookies.remove("jwt");
    }
    this.ready = true;
  },

  methods: {
    logout() {
      OpenAPI.TOKEN = undefined;
      this.$cookies.remove("jwt");
      this.$router.push("/login");
    },

    annotate(task: Task) {
      this.task = task;
      this.page = "task";
    },
  },
});
</script>

<template>
  <i-layout>
    <i-layout-header>
      <i-row center middle>
        <i-column md="3"></i-column>
        <i-column md="6">
          <h1 class="_text-align:center">Annoto</h1>
        </i-column>
        <i-column md="3">
          <i-button v-if="isLoggedIn" id="logout-button" @click="logout">
            Logout
          </i-button>
        </i-column>
      </i-row>
    </i-layout-header>
    <i-layout-content>
      <router-view v-if="ready"></router-view>
      <div v-else>Checking Authentication, please wait...</div>
      <!-- <LoginView
        v-if="page == 'login'"
        id="login-view"
        @login="login"
      ></LoginView>
      <TasksOverView
        v-else-if="page == 'tasks'"
        id="tasks-overview"
        @annotate="annotate"
      ></TasksOverView>
      <TaskView
        v-else-if="page == 'task' && task"
        id="task-view"
        :task="task"
        competency="Prof. Dr. med."
      ></TaskView>
      <div v-else>Invalid Page</div> -->
    </i-layout-content>
  </i-layout>
</template>
