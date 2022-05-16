<script lang="ts">
import { defineComponent } from "vue";

// This component outputs a string with user information (fullname)

export default defineComponent({
  props: {
    fullname: { type: String, required: true },
  },
});
</script>

<template>
  <div>
    Current logged in user:
    <label id="userLabel">{{ fullname }}</label>
  </div>
</template>

<style>
#userLabel {
  color: gray;
}
</style>
