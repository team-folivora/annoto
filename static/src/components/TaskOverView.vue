<script lang="ts">
import { defineComponent } from "vue";
import { TasksService as API } from "@/api/services/TasksService";
import TaskCard from "@/components/TaskCard.vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import type { Task } from "@/api/models/Task";
import { fullname } from "@/utils/helpers";
export default defineComponent({
  data() {
    return {
      tasks: [] as Task[],
    };
  },

  components: {
    TaskCard,
    UserInformationLabel,
  },

  computed: {
    fullname() {
      return fullname();
    },
  },

  mounted() {
    this.fetchTasks();
  },

  methods: {
    async fetchTasks() {
      this.tasks = await API.getTasks();
    },

    annotate(task: Task) {
      this.$emit("annotate", task)
    },
  },
});
</script>

<template>
  <i-layout-content>
    <UserInformationLabel :fullname="fullname" />
    <div class="_display:flex" v-if="tasks.length != 0">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        class="_margin:1"
        @annotate="annotate"
        :id="`task-${task.id}`"
      />
    </div>
    <i-card v-else id="no-more-images" class="margin-y:20px">No more Tasks to accomplish.</i-card>
  </i-layout-content>
</template>
