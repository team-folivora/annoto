<script setup lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import AnnotationButton from "./components/AnnotationButton.vue";
</script>

<template>
  <i-layout>
    <i-layout-header>
      <h1 class="_text-align:center">Annoto</h1>
    </i-layout-header>
    <i-layout-content>
      <ImageDisplay src="http://localhost:5000/images/sloth.jpg" />
      <AnnotationButton
        label="Faultier"
        src="http://localhost:5000/images/sloth.jpg"
      />
      <AnnotationButton
        label="Hund"
        src="http://localhost:5000/images/sloth.jpg"
      />
      <AnnotationButton
        label="Katze"
        src="http://localhost:5000/images/sloth.jpg"
      />
      <AnnotationButton
        label="Maus"
        src="http://localhost:5000/images/sloth.jpg"
      />
    </i-layout-content>
  </i-layout>
</template>
