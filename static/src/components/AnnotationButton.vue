<script lang="ts">
import { defineComponent } from "vue";
import { sha256 } from "js-sha256";
import { TasksService as API } from "../api/services/TasksService";
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
    competency: { type: String, required: true },
    isAttentive: { type: Boolean, required: true },
    username: { type: String, required: true },
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
        let blob = await API.getImage('ecg-qrs-classification-physiodb', this.src);
        let buffer = await blob.arrayBuffer();
        let hash = sha256(buffer);
        await API.saveAnnotation('ecg-qrs-classification-physiodb', this.src, {
          label: this.label,
          hash: hash,
          competency: this.competency,
          is_attentive: this.isAttentive,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
});
</script>

<template>
  <i-button :loading="isLoading" @click="saveAnnotation">Label: {{ label }}</i-button>
</template>
