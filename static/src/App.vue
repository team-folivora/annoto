<script lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import { defineComponent } from "vue";
import { getUrl } from "./utils/helpers";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    ImageDisplay,
    AnnotationButton,
  },

  data() {
    let imageId = "sloth.jpg";
    return {
      labels: ["Faultier", "Hund", "Katze", "Maus"],
      imageId,
      imageSrc: getUrl("images/" + imageId),
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
      <ImageDisplay :src="imageSrc" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :key="label"
          :label="label"
          :src="imageId"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
