<script lang="ts">
import { defineComponent } from "vue";
import ProofOfCondition from "@/components/ProofOfCondition.vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import ImageClassificationTaskView from "@/components/ImageClassificationTaskView.vue";
import FHIRECGAnnotationTaskView from "@/components/FHIRECGAnnotationTaskView.vue";
import { TasksService as API } from "@/api/services/TasksService";
import type { BaseTask } from "@/api/models/BaseTask";
import type { ImageTask } from "@/api/models/ImageTask";
import { paramCase } from "change-case";
import { fullname } from "@/utils/helpers";

export default defineComponent({
  components: {
    ProofOfCondition,
    UserInformationLabel,
    ImageClassificationTaskView,
    FHIRECGAnnotationTaskView,
  },

  data() {
    return {
      visible: true,
      isAttentive: false,
      isTrained: false,
      isLoading: false,
      isError: false,
      task: undefined as BaseTask | void,
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
        console.log(this.task);
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
    <ImageClassificationTaskView
      v-else
      :isAttentive="isAttentive"
      :isTrained="isTrained"
      :task="(task as any)"
    />
  </div>
</template>
