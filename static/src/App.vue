<script lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import { defineComponent } from "vue";

/**
 * The main App component for the website
 */
export default defineComponent({
  data() {
    return {
      labels: ["Faultier", "Hund", "Katze", "Maus"],
    };
  },

  components: {
    ImageDisplay,
    AnnotationButton,
  },
});
</script>

<template>
  <i-layout>
    <i-layout-header>
      <h1 class="_text-align:center">Annoto</h1>
    </i-layout-header>
    <i-layout-content>
      <ImageDisplay src="http://localhost:5000/images/sloth.jpg" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :label="label"
          src="http://localhost:5000/images/sloth.jpg"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
