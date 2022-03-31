<script setup lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
</script>

<template>
  <main>
    <header>annoto</header>
    <ImageDisplay src="http://127.0.0.1:5000/images/sloth.jpg" />
    <AnnotationButton label="Faultier" src="http://127.0.0.1:5000/images/sloth.jpg" />
    <AnnotationButton label="Hund" src="http://127.0.0.1:5000/images/sloth.jpg" />
    <AnnotationButton label="Katze" src="http://127.0.0.1:5000/images/sloth.jpg" />
    <AnnotationButton label="Maus" src="http://127.0.0.1:5000/images/sloth.jpg" />
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
