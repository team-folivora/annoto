<script lang="ts">
import { defineComponent } from "vue";
import { store } from "@/utils/store";

export default defineComponent({
  async mounted() {
    if (store.isLoggedIn) {
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
