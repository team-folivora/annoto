<script setup lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
</script>

<template>
  <main>
    <header>annoto</header>
    <ImageDisplay src="http://127.0.0.1:5000/image" />
    <AnnotationButton text="Faultier" />
    <AnnotationButton text="Hund" />
    <AnnotationButton text="Katze" />
    <AnnotationButton text="Maus" />
  </main>
</template>

<style>
@import "./assets/base.css";

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;

  font-weight: normal;
}

header {
  font-size: xx-large;
  text-align: center;
}

main {
  margin: 0 auto;
}
</style>
