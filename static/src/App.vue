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
    };
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
        @login="page = 'task'"
      ></LoginView>
      <TaskView
        v-else
        id="task-view"
        task-id="ecg-qrs-classification-physiodb"
        competency="Prof. Dr. Med."
        user="AnnotoUser#1337"
      ></TaskView>
    </i-layout-content>
  </i-layout>
</template>
