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

  data() {
    return {
      isLoading: false,
    };
  },

  methods: {
    /**
     * Gets executed when the user clicks on the button
     * annotates the image with the specified label in `label` by calling the api
     */
    async saveAnnotation(): Promise<void> {
      this.isLoading = true;
      try {
        let response = await fetch(`${this.src}?`); // FIXME: Hacky solution to ensure that the browser will not use the previously cached response of a img<src> that would lead to CORS errors
        let blob = await response.blob();
        let buffer = await blob.arrayBuffer();
        let hash = sha256(buffer);
        await axios.post(this.src, {
          label: this.label,
          hash: hash,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
});
</script>

<template>
  <i-button :loading="isLoading" @click="saveAnnotation">
    Label: {{ label }}
  </i-button>
</template>
