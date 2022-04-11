<script lang="ts">
import { defineComponent } from "vue";
import { sha256 } from "js-sha256";
import ToastNotification from "./ToastNotification.vue";
import { DefaultService as API } from "../api/services/DefaultService";
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  components: {
    ToastNotification,
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
      toastType: "success",
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
        this.animateToast(false);
      } catch (e) {
        this.animateToast(true);
        throw(e);
      } finally {
        this.isLoading = false;
      }
    },

    animateToast(isError: Boolean) {
      this.toastType = isError ? "error" : "success";
      this.showToast = true;
      setTimeout(() => {
        this.showToast = false;
      }, 3000);
    },
  },
});
</script>

<template>
  <i-button :loading="isLoading" :disabled="isLoading" @click="saveAnnotation">
    <ToastNotification :visible="showToast" style="text-align: left" :type="toastType" />
    Label: {{ label }}
  </i-button>
</template>
