<script lang="ts">
import { defineComponent } from "vue";
import { TasksService as API } from "@/api/services/TasksService";
import TaskCard from "@/components/TaskCard.vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import type { Task } from "@/api/models/Task";
import { fullname } from "@/utils/helpers";
export default defineComponent({
  components: {
    TaskCard,
    UserInformationLabel,
  },

  emits: ["annotate"],

  data() {
    return {
      tasks: [] as Task[],
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

    annotate(task: Task) {
      this.$emit("annotate", task);
    },
  },
});
</script>

<template>
  <i-layout-content>
    <UserInformationLabel :fullname="fullname() ?? 'Unknown user'" />
    <div v-if="tasks.length != 0" class="_display:flex">
      <TaskCard
        v-for="task in tasks"
        :id="`task-${task.id}`"
        :key="task.id"
        :task="task"
        class="_margin:1"
        @annotate="annotate"
      />
    </div>
    <i-card v-else id="no-more-tasks" class="margin-y:20px">
      No more Tasks to accomplish.
    </i-card>
  </i-layout-content>
</template>
