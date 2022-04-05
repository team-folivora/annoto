<script>
import { defineComponent } from "vue";

// Displays an mocked username on the mainpage

export default defineComponent({
  props: {
    username: { type: String, required: true },
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
