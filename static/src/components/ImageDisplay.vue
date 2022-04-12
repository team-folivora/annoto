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
  <img v-if="src.endsWith('null')" :src="src" />
  <i-card v-else class="margin-y:20px">No more Images to label</i-card>
</template>

<style scoped>
img {
  width: 90vmin;
  margin: 20px auto;
  display: block;
}
</style>
