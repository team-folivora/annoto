<script>
import { defineComponent } from "vue";

// This component outputs a string with user information (username)

export default defineComponent({
  props: {
    username: { type: String, required: true },
  },
});
</script>

<template>
  <div>
    Current logged in user:
    <label id="userLabel" for="username">{{ username }}</label>
  </div>
</template>

<style>
label[for="username"] {
  color: gray;
}
</style>
