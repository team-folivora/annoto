<script lang="ts">
import { defineComponent } from "vue";
import TaskView from "./components/TaskView.vue";
import LoginView from "./components/LoginView.vue";

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
      userName: "",
    };
  },
  methods: {
    onLogin(userName: string) {
      this.page = "tasks";
      this.userName = userName;
    },
  }
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
        @login="onLogin"
      ></LoginView>
      <TaskView
        v-else
        id="task-view"
        task-id="ecg-qrs-classification-physiodb"
        competency="Prof. Dr. Med."
        :user="userName"
      ></TaskView>
    </i-layout-content>
  </i-layout>
</template>
