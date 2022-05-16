<script lang="ts">
import { defineComponent } from "vue";
import { TasksService as API } from "@/api/services/TasksService";
import { OpenAPI } from "@/api";
import { parseJwt } from "@/utils/helpers";
export default defineComponent({
  data() {
    return {
      tasks: [],
    };
  },

  computed: {
    fullname() {
      if (typeof OpenAPI.TOKEN === "string") {
        return parseJwt(OpenAPI.TOKEN)["fullname"];
      } else {
        return undefined;
      }
    },
  },

  mounted() {
    this.fetchTasks();
  },

  methods: {
    async fetchTasks() {
      let task = await API.getTasks();
      console.log(task);
      this.tasks = task;
    },
  },
});
</script>

<template>
  <i-layout-content>
    <UserInformationLabel :fullname="fullname" />
    <div v-if="tasks.length != 0">
    </div>
    <i-card v-else id="no-more-images" class="margin-y:20px">
      No more Tasks to accomplish.
    </i-card>
  </i-layout-content>
</template>
