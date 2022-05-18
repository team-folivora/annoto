<script lang="ts">
import { defineComponent } from "vue";
import type { Task } from "@/api/models/Task";
import { PingService } from "@/api";

/**
 * The main App component for the website
 */
export default defineComponent({
  data() {
    return {
      task: undefined as Task | undefined,
      ready: false,
    };
  },

  async mounted() {
    this.$store.initialize(this.$cookies);
    if (this.$store.jwt) {
      try {
        await PingService.ping();
      } catch (_) {
        this.$store.jwt = undefined;
      }
    } else {
      this.$store.jwt = undefined;
    }
    this.ready = true;
  },

  methods: {
    logout() {
      this.$store.jwt = undefined;
      this.$router.push("/login");
    },
  },
});
</script>

<template>
  <i-layout>
    <i-layout-header>
      <i-row center middle>
        <i-column md="3"></i-column>
        <i-column md="6">
          <h1 class="_text-align:center">Annoto</h1>
        </i-column>
        <i-column md="3">
          <i-button v-if="$store.isLoggedIn" id="logout-button" @click="logout">
            Logout
          </i-button>
        </i-column>
      </i-row>
    </i-layout-header>
    <i-layout-content>
      <router-view v-if="ready"></router-view>
      <div v-else>Checking Authentication, please wait...</div>
    </i-layout-content>
  </i-layout>
</template>
