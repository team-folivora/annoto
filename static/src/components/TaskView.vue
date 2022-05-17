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

  data() {
    return {
      visible: true,
      isAttentive: false,
      isTrained: false,
      imageId: undefined as string | void,
      task: undefined as Task | undefined,
    };
  },

  async mounted() {
    this.$watch(() => this.$route.params, this.fetchTask);
    await this.fetchTask();
  },

  methods: {
    async fetchTask() {
      const id = this.$route.params["taskid"];
      if (typeof id !== "string") return;
      this.task = await API.getTask(id);
      await this.nextImage();
    },

    async nextImage() {
      if (!this.task) return;
      this.imageId = await API.getNextImage(this.task.id).catch((e) => {
        console.log(e);
        this.imageId = undefined;
      });
    },

    fullname,

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
    <UserInformationLabel :fullname="fullname() ?? 'Unknown user'" />
    <div v-if="imageId && task">
      <ImageDisplay id="image-display" :task-id="task.id" :image-id="imageId" />
      <i-button-group block>
        <AnnotationButton
          v-for="label in task.labels"
          :id="'annotation-button-' + paramCase(label)"
          :key="label"
          :label="label"
          :is-attentive="isAttentive"
          :is-trained="isTrained"
          :competency="'Prof. Dr. Med.'"
          :task-id="task!.id"
          :image-id="imageId!"
          @annotation-saved="nextImage"
        />
      </i-button-group>
    </div>
    <i-card v-else id="no-more-images" class="margin-y:20px">
      No more Images to label
    </i-card>
  </i-layout-content>
</template>
