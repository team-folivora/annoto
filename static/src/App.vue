<script lang="ts">
import ImageDisplay from "@/components/ImageDisplay.vue";
import AnnotationButton from "@/components/AnnotationButton.vue";
import ProofOfCondition from "@/components/ProofOfCondition.vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import { defineComponent } from "vue";
import { TasksService as API } from "@/api/services/TasksService";
import { paramCase } from "change-case";

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

  props: {
    taskId: { type: String, required: true },
    competency: { type: String, required: true },
    user: { type: String, required: true },
  },

  data() {
    return {
      labels: [] as string[],
      visible: true,
      isAttentive: false,
      isTrained: false,
      imageId: undefined as string | undefined,
    };
  },

  mounted() {
    this.fetchLabels();
    this.nextImage();
  },

  methods: {
    async fetchLabels() {
      let task = await API.getTask(this.taskId);
      this.labels = task.labels;
    },

    async nextImage() {
      this.imageId = await API.getNextImage(this.taskId).catch((e) => {
        console.log(e);
        delete this.imageId;
      });
    },

    paramCase,
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
      <UserInformationLabel :username="user" />
      <div v-if="imageId">
        <ImageDisplay
          id="image-display"
          :task-id="taskId"
          :image-id="imageId"
        />
        <i-button-group block>
          <AnnotationButton
            v-for="label in labels"
            :id="'annotation-button-' + paramCase(label)"
            :key="label"
            :label="label"
            username="user"
            :is-attentive="isAttentive"
            :is-trained="isTrained"
            :competency="competency"
            :task-id="taskId"
            :image-id="imageId"
            @annotation-saved="nextImage"
          />
        </i-button-group>
      </div>
      <i-card v-else id="no-more-images" class="margin-y:20px">
        No more Images to label
      </i-card>
    </i-layout-content>
  </i-layout>
</template>
