<script setup lang="ts">
defineProps<{
  src: string;
}>();
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
