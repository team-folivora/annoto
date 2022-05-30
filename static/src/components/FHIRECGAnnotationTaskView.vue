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
      // get next observation stuff
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
      width="100%"
      height="100%"
      frameborder="0"
    ></iframe>
  </div>
</template>

<style scoped>
div {
  height: 80vh;
}
</style>
