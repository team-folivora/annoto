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
      isLoading: false,
      isError: false,
      imageId: undefined as string | void,
      task: undefined as Task | void,
    };
  },

  async mounted() {
    this.$watch(() => this.$route.params, this.fetchTask);
    await this.fetchTask();
  },

  methods: {
    async fetchTask() {
      try {
        this.isLoading = true;
        const id = this.$route.params["taskId"];
        if (typeof id !== "string") throw Error();
        this.task = await API.getTask(id);
        await this.nextImage();
      } catch {
        this.isError = true;
      } finally {
        this.isLoading = false;
      }
    },

    async nextImage() {
      try {
        this.isLoading = true;
        this.imageId = undefined;
        if (!this.task) throw Error();
        this.imageId = await API.getNextImage(this.task.id).catch(console.log);
      } catch {
        this.isError = true;
      } finally {
        this.isLoading = false;
      }
    },

    fullname,

    paramCase,
  },
});
</script>

<template>
  <div id="task-view">
    <ProofOfCondition
      v-model:isAttentive="isAttentive"
      v-model:isTrained="isTrained"
    />
    <UserInformationLabel :fullname="fullname() ?? 'Unknown user'" />
    <div v-if="isError">
      <i-card class="margin-y:20px">An Error occured</i-card>
    </div>
    <div v-else-if="isLoading">
      <i-loader />
    </div>
    <i-card
      v-else-if="imageId === undefined"
      id="no-more-images"
      class="margin-y:20px"
    >
      No more Images to label
    </i-card>
    <div v-else>
      <ImageDisplay
        id="image-display"
        :task-id="task!.id"
        :image-id="imageId"
      />
      <i-button-group block>
        <AnnotationButton
          v-for="label in task!.labels"
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
  </div>
</template>
