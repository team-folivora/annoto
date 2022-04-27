<script lang="ts">
import { defineComponent } from "vue";
import TaskPane from "./components/TaskPane.vue";
import LoginPane from "./components/LoginPane.vue";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    TaskPane,
    LoginPane,
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
    <LoginPane
      v-if="page == 'login'"
      id="login-view"
      :page="page"
      @login="page = 'task'"
    ></LoginPane>
    <TaskPane
      v-else
      id="task-view"
      task-id="ecg-qrs-classification-physiodb"
      competency="Prof. Dr. Med."
      user="AnnotoUser#1337"
    ></TaskPane>
  </i-layout>
</template>
