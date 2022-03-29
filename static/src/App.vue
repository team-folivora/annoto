<script setup lang="ts">
import ImageDisplay from "./components/ImageDisplay.vue";
import ButtonCounter from "./components/ButtonCounter.vue";
</script>

<template>
  <main>
    <header>annoto</header>
    <ImageDisplay src="http://127.0.0.1:5000/image" />
    <ButtonCounter text="Faultier"/>
    <ButtonCounter text="Hund"/>
    <ButtonCounter text="Katze"/>
    <ButtonCounter text=""/>
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
