<script lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import { defineComponent } from "vue";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    ImageDisplay,
    AnnotationButton,
  },

  data() {
    return {
      labels: ["Faultier", "Hund", "Katze", "Maus"],
      apiUrl: import.meta.env.VITE_API_URL?.toString() || "",
      imageSrc: "sloth.jpg",
    };
  },
});
</script>

<template>
  <i-layout>
    <i-layout-header>
      <h1 class="_text-align:center">Annoto</h1>
    </i-layout-header>
    <i-layout-content>
      <ImageDisplay :src="apiUrl + 'images/' + imageSrc + '?'" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :key="label"
          :label="label"
          :src="imageSrc"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
