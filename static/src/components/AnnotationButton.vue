<script lang="ts">
import axios from 'axios';
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
    label: { type: String, required: true }
  },

  methods: {
    /**
     * Gets executed when the user clicks on the button
     * annotates the image with the specified label in `label` by calling the api
     */
    async saveAnnotation(): Promise<void> {
      // somewhere define the current image and pass it into here
      await axios.get('http://localhost:5000/images/sloth.jpg')
        .then(function (response) {
          // handle success
          console.log(response);
        });
    }
  }
})
</script>

<template>
  <button @click="saveAnnotation">Label: {{ label }}</button>
</template>

<style scoped>
button {
  margin: 10px;
}
</style>
