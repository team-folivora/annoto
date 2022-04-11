<script lang="ts">
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
    <label id="userLabel">{{ username }}</label>
  </div>
</template>

<style>
#userLabel {
  color: gray;
}
</style>
