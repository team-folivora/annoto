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
  <div>
    <img :src="src[0].value" />
  </div>
</template>

<style scoped>
div {
  height: 70vmin;
  width: 100%;
  margin: 20px auto;
}

img {
  display: block;
  object-fit: contain;
  width: 100%;
  height: 100%;
}
</style>
