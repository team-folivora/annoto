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
        axios({
          method: 'post',
          url: 'http://localhost:5000/images/sloth.jpg',
          data: {
            label: this.label,
            hash: "e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
          }
        })  
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
