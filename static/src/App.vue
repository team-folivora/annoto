<script lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import ProofOfAttentiveness from "./components/ProofOfAttentiveness.vue";
import UserInformationLabel from "./components/UserInformationLabel.vue";
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
    UserInformationLabel,
  },

  data() {
    let imageId = "sloth.jpg";
    return {
      labels: ["Faultier", "Hund", "Katze", "Maus"],
      visible: true,
      isAttentive: false,
      competency: "Prof. Dr. Med.",
      user: "AnnotoUser#1337",
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
      <UserInformationLabel :username="user" />
      <ImageDisplay id="image-display" :src="imageSrc" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :id="'annotation-button-' + label"
          :key="label"
          :label="label"
          :username="user"
          :src="imageId"
          :is-attentive="isAttentive"
          :competency="competency"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
