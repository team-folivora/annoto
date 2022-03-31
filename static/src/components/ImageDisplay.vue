<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    src: { type: String, required: true }
  },
})
</script>

<template>
  <img :src="src"/>
</template>

<style scoped>
img {
  width: 70vw;
  margin: 20px auto;
  display: block;
}
</style>
