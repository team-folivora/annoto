<script lang="ts">
import axios from 'axios';
import { defineComponent } from 'vue';
import shajs from 'sha.js';
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  props: {
    /**
     * The label of the button.
     * Is displayed on the button and passed to the backend to save the annotation.
     */
    label: { type: String, required: true },
    src: { type: String, required: true }
  },

  methods: {
    /**
     * Gets executed when the user clicks on the button
     * annotates the image with the specified label in `label` by calling the api
     */
    async saveAnnotation(): Promise<void> {
      // somewhere define the current image and pass it into here
        let file = await axios.get(this.src)
        console.log(file)
        console.log(shajs('sha256').update(file).digest('hex'))
        axios({
          method: 'post',
          url: this.src,
          data: {
            label: this.label,
            hash: shajs('sha256').update(file).digest('hex'), //"e922903b4d5431a8f9def3c89ffcb0b18472f3da304f28a2dbef9028b6cd205d",
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
