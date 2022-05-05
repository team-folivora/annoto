<script lang="ts">
import { defineComponent, ref } from "vue";
import { TasksService as API } from "@/api/services/TasksService";
import { computedAsync } from "@vueuse/core";

/**
 * Displays an image specified by `src`
 */
export default defineComponent({
  props: {
    /**
     * Task from which an image should be loaded.
     */
    taskId: { type: String, required: true },
    /**
     * Image that should be loaded.
     */
    imageId: { type: String, required: true },
  },

  data() {
    return {
      src: [ref<string | undefined>(undefined)],
    };
  },

  mounted() {
    this.src = [
      computedAsync(async () => {
        let image = await API.getImage(this.taskId, this.imageId);
        return image ? URL.createObjectURL(image) : undefined;
      }, undefined),
    ];
  },
});
</script>

<template>
  <img :src="src[0].value" />
</template>

<style scoped>
img {
  width: 90vmin;
  margin: 20px auto;
  display: block;
}
</style>
