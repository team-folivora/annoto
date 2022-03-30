<script setup lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import Button from "./components/Button.vue";
</script>

<template>
  <main>
    <header>annoto</header>
    <ImageDisplay src="http://127.0.0.1:5000/image" />
    <Button text="Faultier" />
    <Button text="Hund" />
    <Button text="Katze" />
    <Button text="Maus" />
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
