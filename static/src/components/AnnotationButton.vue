<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";
import { sha256 } from "js-sha256";
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  props: {
    /**
     * The label of the button.
     * Is displayed on the button and passed to the backend to save the annotation.
     */
    label: { type: String, required: true },
    src: { type: String, required: true },
  },

  methods: {
    /**
     * Gets executed when the user clicks on the button
     * annotates the image with the specified label in `label` by calling the api
     */
    async saveAnnotation(): Promise<void> {
      let response = await fetch(this.src.replaceAll("images", "imagesx"));
      let blob = await response.blob();
      let buffer = await blob.arrayBuffer();
      let hash = sha256(buffer);
      await axios({
        method: "post",
        url: this.src,
        data: {
          label: this.label,
          hash: hash,
        },
      });
    },
  },
});
</script>

<template>
  <button @click="saveAnnotation">Label: {{ label }}</button>
</template>

<style scoped>
button {
  margin: 10px;
}
</style>
