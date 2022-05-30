<script lang="ts">
import { defineComponent } from "vue";
import ImageDisplay from "@/components/ImageDisplay.vue";
import AnnotationButton from "@/components/AnnotationButton.vue";
import type { ImageTask } from "@/api/models/ImageTask";
import { TasksService as API } from "@/api/services/TasksService";
import { paramCase } from "change-case";

export default defineComponent({
  components: {
    ImageDisplay,
    AnnotationButton,
  },

  props: {
    /**
     * Specifies whether the user is attentive and has finished the training
     */
    isAttentive: { type: Boolean, required: true },
    isTrained: { type: Boolean, required: true },
    task: { type: Object as () => ImageTask, required: true },
  },

  data() {
    return {
      isLoading: false,
      isError: false,
      imageId: undefined as string | void,
    };
  },

  async mounted() {
    await this.nextImage(); //don't know if this is good, probably not
  },

  methods: {
    async nextImage() {
      try {
        this.isLoading = true;
        this.imageId = undefined;
        if (!this.task) throw Error();
        this.imageId = await API.getNextSample(this.task.id).catch(console.log);
      } catch {
        this.isError = true;
      } finally {
        this.isLoading = false;
      }
    },

    paramCase,
  },
});
</script>

<template>
  <i-card
    v-if="imageId === undefined"
    id="no-more-images"
    class="margin-y:20px"
  >
    No more Images to label
  </i-card>
  <div v-else>
    <ImageDisplay id="image-display" :task-id="task!.id" :image-id="imageId" />
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
</template>
