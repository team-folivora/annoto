<script lang="ts">
import { defineComponent } from "vue";
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import UserInformationLabel from "./components/UserInformationLabel.vue";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    ImageDisplay,
    AnnotationButton,
    UserInformationLabel,
  },

  data() {
    return {
      labels: ["Faultier", "Hund", "Katze", "Maus"],
      user: "AnnotoUser#1337",
      apiUrl: import.meta.env.VITE_API_URL?.toString() || "",
      imageUrl: "images/sloth.jpg",
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
      <i-label-group block>
        <UserInformationLabel :username="user" />
      </i-label-group>
      <ImageDisplay id="image-display" :src="apiUrl + imageUrl" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :key="label"
          :label="label"
          :id="'annotation-button-' + label"
          :username="user"
          :src="apiUrl + imageUrl"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
