<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    text: { type: String, required: true }
  },

  methods: {
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
