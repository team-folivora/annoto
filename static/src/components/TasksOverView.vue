<script lang="ts">
import { defineComponent } from "vue";
import { TasksService as API } from "@/api/services/TasksService";
import TaskCard from "@/components/TaskCard.vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import type { BaseTask } from "@/api/models/BaseTask";
import { fullname } from "@/utils/helpers";
export default defineComponent({
  components: {
    TaskCard,
    UserInformationLabel,
  },

  data() {
    return {
      tasks: [] as BaseTask[],
    };
  },

  mounted() {
    this.fetchTasks();
  },

  methods: {
    async fetchTasks() {
      this.tasks = await API.getTasks();
    },

    fullname,
  },
});
</script>

<template>
  <div id="tasks-overview">
    <UserInformationLabel :fullname="fullname() ?? 'Unknown user'" />
    <div v-if="tasks.length != 0" class="_display:flex _flex-wrap:wrap">
      <TaskCard
        v-for="task in tasks"
        :id="`task-${task.id}`"
        :key="task.id"
        :task="task"
        class="_margin:1 _width:25% _flex-grow:1"
      />
    </div>
    <i-card
      v-else
      id="no-more-tasks"
      color="success"
      class="_margin-x:auto _margin-y:4 _width:25%"
    >
      <template #header>Done!</template>
      No more Tasks to accomplish.
    </i-card>
  </div>
</template>
