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
    </template>
    {{ task.description }}
    <br />
    Type: {{ task.type_id }}
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
