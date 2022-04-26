<script lang="ts">
import { defineComponent } from "vue";
import TaskPane from "./components/TaskPane.vue";
import LoginPane from "./components/LoginPane.vue";

/**
 * The main App component for the website
 */
export default defineComponent({
  data() {
    return {
      page: "login",
    };
  },
  components: {
    TaskPane,
    LoginPane,
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
      :page="page"
      @login="page = 'task'"
    ></LoginPane>
    <TaskPane
      taskId="ecg-qrs-classification-physiodb"
      competency="Prof. Dr. Med."
      user="AnnotoUser#1337"
      v-else
    ></TaskPane>
  </i-layout>
</template>
