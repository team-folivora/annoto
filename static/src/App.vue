<script setup lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
</script>

<template>
  <main>
    <header>annoto</header>
    <ImageDisplay src="http://localhost:5000/images/sloth.jpg" />
    <AnnotationButton label="Faultier" src="http://localhost:5000/images/sloth.jpg" />
    <AnnotationButton label="Hund" src="http://localhost:5000/images/sloth.jpg" />
    <AnnotationButton label="Katze" src="http://localhost:5000/images/sloth.jpg" />
    <AnnotationButton label="Maus" src="http://localhost:5000/images/sloth.jpg" />
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
