<script lang="ts">
import { defineComponent } from "vue";
import ImageDisplay from "@/components/ImageDisplay.vue";
import AnnotationButton from "@/components/AnnotationButton.vue";
import ProofOfCondition from "@/components/ProofOfCondition.vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import { TasksService as API } from "@/api/services/TasksService";
import type { Task } from "@/api/models/Task";
import { paramCase } from "change-case";
import { fullname } from "@/utils/helpers";
export default defineComponent({
  components: {
    ImageDisplay,
    AnnotationButton,
    ProofOfCondition,
    UserInformationLabel,
  },

  props: {
    task: { type: Object as () => Task, required: true },
    competency: { type: String, required: true },
  },

  data() {
    return {
      visible: true,
      isAttentive: false,
      isTrained: false,
      imageId: undefined as string | void,
    };
  },

  computed: {
    fullname() {
      return fullname();
    },
  },

  mounted() {
    this.nextImage();
  },

  methods: {
    async nextImage() {
      this.imageId = await API.getNextImage(this.task.id).catch((e) => {
        console.log(e);
        this.imageId = undefined;
      });
    },

    paramCase,
  },
});
</script>

<template>
  <i-layout-content>
    <ProofOfCondition
      v-model:isAttentive="isAttentive"
      v-model:isTrained="isTrained"
    />
    <UserInformationLabel :fullname="fullname" />
    <div v-if="imageId">
      <ImageDisplay id="image-display" :task-id="task.id" :image-id="imageId" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in task.labels"
          :id="'annotation-button-' + paramCase(label)"
          :key="label"
          :label="label"
          :is-attentive="isAttentive"
          :is-trained="isTrained"
          :competency="competency"
          :task-id="task.id"
          :image-id="imageId"
          @annotation-saved="nextImage"
        />
      </i-button-group>
    </div>
    <i-card v-else id="no-more-images" class="margin-y:20px">
      No more Images to label
    </i-card>
  </i-layout-content>
</template>
