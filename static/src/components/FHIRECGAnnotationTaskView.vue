<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      observationId: undefined as string | void,
      isLoading: false,
      isError: false,
    }
  },

  methods: {
    async nextObservation() {
      // get next observation stuff
      try {
        this.isLoading = true;
        this.Obe = undefined;
        if (!this.task) throw Error();
        this.observationId = await API.getNextOberservation(this.task.id).catch(console.log);
      } catch {
        this.isError == true;
      }
    },
  },
});
</script>

<template>
  // iFrame stuff
  <div class="iframe-container">
    <iframe

      src="https://telemed.intern.synios.eu/ecgviewer/?observationId=285c6909-7ded-4dd8-92a7-a02501676ddb"
      width="80%" height="100" frameborder="0" >
    </iframe>
  </div>
</template>
