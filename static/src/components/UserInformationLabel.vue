<script>
import { defineComponent } from "vue";

// Displays an mocked username on the mainpage

export default defineComponent({
  data() {
    return {
      username: "AnnotoUser#1337",
    };
  },
});
</script>

<template>
  <div>
    Current logged in user: <label for="username"> {{ username }} </label>
  </div>
</template>

<style>
label[for="username"] {
  color: gray;
}
</style>
