<script lang="ts">
import { defineComponent } from "vue";
import type { BaseTask } from "@/api/models/BaseTask";
export default defineComponent({
  props: {
    task: { type: Object as () => BaseTask, required: true },
  },
});
</script>

<template>
  <i-card>
    <template #header>
      {{ task.id }}
      <br />
      <i-badge class="_margin-top:1/4">{{ task.type_id }}</i-badge>
    </template>
    {{ task.description }}
    <template #footer>
      <i-button
        color="primary"
        @click="$router.push({ name: 'Task', params: { taskId: task.id } })"
      >
        Start Annotating
      </i-button>
    </template>
  </i-card>
</template>
