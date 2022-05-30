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
      }
    },
  },
});
</script>

<template>
  <div class="iframe-container">
    <iframe
      src="https://telemed.intern.synios.eu/ecgviewer/?observationId=285c6909-7ded-4dd8-92a7-a02501676ddb"
      width="150%"
      height="150%"
      frameborder="0"
    ></iframe>
  </div>
</template>

<style scoped>
div {
  height: 80vh;
  overflow: hidden;
}
iframe {
  -webkit-transform: scale(calc(1 / 1.5));
  transform: scale(calc(1 / 1.5));
  -webkit-transform-origin: 0 0;
  transform-origin: 0 0;
}
</style>
