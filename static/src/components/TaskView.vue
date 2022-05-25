<script lang="ts">
import { defineComponent } from "vue";
import ProofOfCondition from "@/components/ProofOfCondition.vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import ImageClassificationTaskView from "@/components/ImageClassificationTaskView.vue";
import FHIRECGAnnotationTaskView from "@/components/FHIRECGAnnotationTaskView.vue";
import { TasksService as API } from "@/api/services/TasksService";
import type { BaseTask } from "@/api/models/BaseTask";
import { TaskType } from "@/api/models/TaskType";
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

  computed: {
    taskView() {
      if (this.task) {
        console.log(this.task);
        console.log(this.task.type_id);
        console.log(this.task.type_id == TaskType.IMAGE_CLASSIFICATION);
        //return "Hallo"
        if (this.task.type_id == TaskType.IMAGE_CLASSIFICATION) {
          console.log("Test");
          //return "<div>ImageClassification</div>";
          return '<div><ImageClassificationTaskView :isAttentive="isAttentive" :isTrained="isTrained" :task="(task as ImageTask)"/><div>';
        } else if (this.task.type_id == TaskType.FHIR_ECG_ANNOTATION) {
          return "<div>FIREECG</div>";
        }
      }
    },
  },

  methods: {
    async fetchTask() {
      try {
        this.isLoading = true;
        const id = this.$route.params["taskId"];
        if (typeof id !== "string") throw Error();
        this.task = await API.getTask(id);
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
    <div v-else-if="isLoading"><i-loader /></div>

    <div v-else-if="task.type_id == 'image_classification'">
      <ImageClassificationTaskView
        :isAttentive="isAttentive"
        :isTrained="isTrained"
        :task="(task as ImageTask)"
      />
    </div>
    <div v-else-if="task.type_id == 'fhir_ecg_annotation'">
      <FHIRECGAnnotationTaskView />
    </div>
  </div>
</template>
