<script lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import ProofOfAttentiveness from "./components/ProofOfAttentiveness.vue";
import { defineComponent } from "vue";
import { getUrl } from "./utils/helpers";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    ImageDisplay,
    AnnotationButton,
    ProofOfAttentiveness,
  },

  data() {
    let imageId = "sloth.jpg";
    return {
      labels: ["Faultier", "Hund", "Katze", "Maus"],
      visible: true,
      isAttentive: false,
      competency: "Prof. Dr. Med.",
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
      <ProofOfAttentiveness v-model:isAttentive="isAttentive" />
      <ImageDisplay :src="imageSrc" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :key="label"
          :label="label"
          :src="imageId"
          :isAttentive="isAttentive"
          :competency="competency"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
