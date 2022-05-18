<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  async mounted() {
    const jwt = this.$cookies.get("jwt");
    if (jwt) {
      this.$router.push("/tasks");
    } else {
      this.$router.push("/login");
    }
  },
});
</script>

<template>
  <div>Redirecting, please wait...</div>
</template>
