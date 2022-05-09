<script lang="ts">
import { defineComponent } from "vue";
import { TasksService as API } from "@/api/services/TasksService";
import { paramCase } from "change-case";
import { OpenAPI } from "@/api";
import { parseJwt } from "@/utils/helpers";
export default defineComponent({
  props: {
    taskId: { type: String, required: true },
    competency: { type: String, required: true },
  },

  data() {
    return {
      labels: [] as string[],
      visible: true,
      isAttentive: false,
      isTrained: false,
      imageId: undefined as string | void,
    };
  },

  computed: {
    fullname() {
      if (typeof OpenAPI.TOKEN === "string") {
        return parseJwt(OpenAPI.TOKEN)["fullname"];
      } else {
        return undefined;
      }
    },
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
        this.imageId = undefined;
      });
    },

    paramCase,
  },
});
</script>

<template>
  <ProofOfCondition
    v-model:isAttentive="isAttentive"
    v-model:isTrained="isTrained"
  />
  <UserInformationLabel :fullname="fullname" />
  <div v-if="imageId">
    <el-row justify="center">
      <ImageDisplay id="image-display" :task-id="taskId" :image-id="imageId" />
      <el-button-group>
        <AnnotationButton
          v-for="label in labels"
          :id="'annotation-button-' + paramCase(label)"
          :key="label"
          :label="label"
          :is-attentive="isAttentive"
          :is-trained="isTrained"
          :competency="competency"
          :task-id="taskId"
          :image-id="imageId"
          @annotation-saved="nextImage"
        />
      </el-button-group>
    </el-row>
  </div>
  <el-empty v-else description="No more Images to label" id="no-more-images" />
</template>
