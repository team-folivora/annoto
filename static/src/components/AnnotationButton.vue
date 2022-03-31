<script lang="ts">
import { defineComponent } from 'vue'
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  props: {
    /**
     * The label of the button.
     * Is displayed on the button and passed to the backend to save the annotation.
     */
    text: { type: String, required: true }
  },

  methods: {
    /**
     * Gets executed when the user clicks on the button
     * @param text printed to the console
     */
    log(text: String): void {
      console.log("Hallo Mami" + "-" + text);
    }
  }
})
</script>

<template>
  <button @click="log(text)">Label: {{ text }}</button>
</template>

<style scoped>
  button{
    margin: 10px;
  }
</style>
