<script lang="ts">
import { getUrl } from "@/utils/helpers";
import { defineComponent } from "vue";
/**
 * Displays an image specified by `src`
 */
export default defineComponent({
  computed: {
    src() {
      return getUrl(`tasks/${this.taskId}/${this.imageId}`);
    },
  },
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
});
</script>

<template>
  <img :src="src" />
</template>

<style scoped>
img {
  width: 90vmin;
  margin: 20px auto;
  display: block;
}
</style>
