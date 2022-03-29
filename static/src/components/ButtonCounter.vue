<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
    }
  },

  props: {
    text: { type: String, required: true }
  },

  methods: {
    log(text: String): void {
      console.log("hallo mami" + text);
    }
  }
})
</script>

<template>
  <button @click="log(text)">Label: {{ text }}</button>
</template>