<script setup lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
</script>

<template>
  <i-layout>
    <i-layout-header>
      <h1 class="_text-align:center">Annoto</h1>
    </i-layout-header>
    <i-layout-content>
      <ImageDisplay src="http://127.0.0.1:5000/image" />
    </i-layout-content>
  </i-layout>
</template>
