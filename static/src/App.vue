<script lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
import ProofOfCondition from "./components/ProofOfCondition.vue";
import UserInformationLabel from "./components/UserInformationLabel.vue";
import { defineComponent } from "vue";
import { getUrl } from "./utils/helpers";
import { TasksService as API } from "./api/services/TasksService";

/**
 * The main App component for the website
 */
export default defineComponent({
  components: {
    ImageDisplay,
    AnnotationButton,
    ProofOfCondition,
    UserInformationLabel,
  },

  data() {
    let imageId = "sloth.jpg";
    let labels: string[] = [];
    this.fetch_labels();
    return {
      labels: labels,
      visible: true,
      isAttentive: false,
      isTrained: false,
      competency: "Prof. Dr. Med.",
      user: "AnnotoUser#1337",
      imageId,
      imageSrc: getUrl("tasks/ecg-qrs-classification-physiodb/" + imageId),
    };
  },

  methods: {
    async fetch_labels() {
      let task = await API.getTask("ecg-qrs-classification-physiodb");
      this.labels = task.labels;
    },
  },
});
</script>

<template>
  <i-layout>
    <i-layout-header>
      <h1 class="_text-align:center">Annoto</h1>
    </i-layout-header>
    <i-layout-content>
      <ProofOfCondition
        v-model:isAttentive="isAttentive"
        v-model:isTrained="isTrained"
      />
      <i-label-group block>
        <UserInformationLabel :username="user" />
      </i-label-group>
      <ImageDisplay id="image-display" :src="imageSrc" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in labels"
          :id="'annotation-button-' + label.toLowerCase().replace(/\s+/g, '-')"
          :key="label"
          :label="label"
          :username="user"
          :src="imageId"
          :is-attentive="isAttentive"
          :is-trained="isTrained"
          :competency="competency"
        />
      </i-button-group>
    </i-layout-content>
  </i-layout>
</template>
