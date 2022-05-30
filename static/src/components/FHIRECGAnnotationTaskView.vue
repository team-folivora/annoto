<script lang="ts">
import type { FHIRECGTask } from "@/api";
import { defineComponent } from "vue";
import { TasksService as API } from "@/api/services/TasksService";

export default defineComponent({
  props: {
    task: { type: Object as () => FHIRECGTask, required: true },
  },

  data() {
    return {
      observationId: undefined as string | void,
      isLoading: false,
      isError: false,
    };
  },

  async mounted() {
    await this.nextObservation();
  },

  methods: {
    async nextObservation() {
      try {
        this.isLoading = true;
        this.observationId = undefined;
        if (!this.task) throw Error();
        this.observationId = await API.getNextSample(this.task.id).catch(
          console.log
        );
      } catch {
        this.isError == true;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
</script>

<template>
  <div v-if="isError">
    <i-card color="danger" class="_margin-x:auto _margin-y:4 _width:25%">
      <template #header>Error</template>
      An error occured while loading the task.
    </i-card>
  </div>
  <div v-else-if="isLoading">
    <i-loader class="_display:block _margin-x:auto _margin-y:4" />
  </div>
  <i-card
    v-else-if="observationId === undefined"
    id="no-more-images"
    color="success"
    class="_margin-x:auto _margin-y:4 _width:25%"
  >
    <template #header>Done!</template>
    No more ECGs to label
  </i-card>
  <div v-else class="iframe-container">
    <iframe
      :src="`https://telemed.intern.synios.eu/ecgviewer/?observationId=${observationId}`"
      width="150%"
      height="150%"
      frameborder="0"
    ></iframe>
  </div>
  <i-button @click="nextObservation" class="_float:right _margin-top:1">
    Next ➤
  </i-button>
</template>

<style scoped>
.iframe-container {
  height: 75vh;
  overflow: hidden;
}
iframe {
  -webkit-transform: scale(calc(1 / 1.5));
  transform: scale(calc(1 / 1.5));
  -webkit-transform-origin: 0 0;
  transform-origin: 0 0;
}
</style>
