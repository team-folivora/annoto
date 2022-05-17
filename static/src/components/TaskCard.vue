<script lang="ts">
import { defineComponent } from "vue";
import type { Task } from "@/api/models/Task";
export default defineComponent({
  props: {
    task: { type: Object as () => Task, required: true },
  },

  emits: ["annotate"],
});
</script>

<template>
  <i-card>
    <template #header>
      {{ task.id }}
    </template>
    {{ task.description }}
    <template #footer>
      <i-button color="primary" @click="$emit('annotate', task)">
        Start Annotating
      </i-button>
    </template>
  </i-card>
</template>
