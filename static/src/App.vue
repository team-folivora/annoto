<script lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import ProofOfAttentiveness from "./components/ProofOfAttentiveness.vue";
import { defineComponent } from "vue";

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
    return {
      labels: ["Faultier", "Hund", "Katze", "Maus"],
      apiUrl: import.meta.env.VITE_API_URL?.toString() || "",
      imageUrl: "images/sloth.jpg",
      visible: true,
      isAttentive: false,
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
      <ProofOfAttentiveness v-model:isAttentive="isAttentive"/>
      <ImageDisplay :src="apiUrl + imageUrl" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :key="label"
          :label="label"
          :src="apiUrl + imageUrl"
          v-model:isAttentive="isAttentive"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
