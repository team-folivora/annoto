<script lang="ts">
import { defineComponent } from "vue";
/**
 * Displays an image specified by `src`
 */
export default defineComponent({
  props: {
    /**
     * Source from where the image should be loaded.
     */
    src: { type: String, required: true },
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
