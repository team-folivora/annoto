<script lang="ts">
import { defineComponent } from "vue";
import { sha256 } from "js-sha256";
import { TasksService as API } from "@/api/services/TasksService";
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  props: {
    /**
     * The label of the button.
     * Is displayed on the button and passed to the backend to save the annotation.
     * The other properties are transmitted for the annotation in the api.
     */
    label: { type: String, required: true },
    taskId: { type: String, required: true },
    imageId: { type: String, required: true },
    competency: { type: String, required: true },
    isAttentive: { type: Boolean, required: true },
    isTrained: { type: Boolean, required: true },
  },

  emits: ["annotationSaved"],

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
        let blob = await API.getImage(this.taskId, this.imageId);
        let buffer = await blob.arrayBuffer();
        let hash = sha256(buffer);
        await API.saveAnnotation(this.taskId, this.imageId, {
          label: this.label,
          hash: hash,
          is_trained: this.isTrained,
          competency: this.competency,
          is_attentive: this.isAttentive,
        });
        this.$emit("annotationSaved");
        this.$toast?.success("Annotation successfully saved.");
      } catch (e) {
        this.$toast?.danger("Something went wrong. Annotation not saved.");
        throw e;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
</script>

<template>
  <i-button :loading="isLoading" :disabled="isLoading" @click="saveAnnotation">
    Label: {{ label }}
  </i-button>
</template>
