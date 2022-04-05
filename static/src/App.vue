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
      <UserInformationLabel :username="user" />
      <ImageDisplay src="http://localhost:5000/images/sloth.jpg" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :key="label"
          :label="label"
          :username="user"
          src="http://localhost:5000/images/sloth.jpg"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
