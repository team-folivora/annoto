<script lang="ts">
import { defineComponent } from "vue";
import { sha256 } from "js-sha256";
import Toast from "./Toast.vue";
import { DefaultService as API } from "../api/services/DefaultService";
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  components: {
    Toast,
  },

  props: {
    /**
     * The label of the button.
     * Is displayed on the button and passed to the backend to save the annotation.
     */
    label: { type: String, required: true },
    src: { type: String, required: true },
    username: { type: String, required: true },
  },

  data() {
    return {
      isLoading: false,
      showToast: false,
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
        let blob = await API.getImage(this.src);
        let buffer = await blob.arrayBuffer();
        let hash = sha256(buffer);
        await API.saveAnnotation(this.src, {
          label: this.label,
          hash: hash,
        });
      } finally {
        this.isLoading = false;
        this.showToast = true;
        setTimeout(() => {
          this.showToast = false;
        }, 3000);
      }
    },
  },
});
</script>

<template>
  <i-button :loading="isLoading" :disabled="isLoading" @click="saveAnnotation">
    <Toast :visible="showToast" style="text-align: left" />
    Label: {{ label }}
  </i-button>
</template>
