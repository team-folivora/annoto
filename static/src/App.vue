<script lang="ts">
import { defineComponent } from "vue";
import type { Task } from "@/api/models/Task";
import { OpenAPI, PingService } from "@/api";
import { isLoggedIn } from "@/utils/store";

/**
 * The main App component for the website
 */
export default defineComponent({
  data() {
    return {
      task: undefined as Task | undefined,
      ready: false,
      isLoggedIn,
    };
  },

  async mounted() {
    const jwt = this.$cookies.get("jwt");
    if (jwt) {
      try {
        OpenAPI.TOKEN = jwt;
        await PingService.ping();
      } catch (_) {
        OpenAPI.TOKEN = undefined;
        this.$cookies.remove("jwt");
      }
    } else {
      this.$cookies.remove("jwt");
    }
    this.ready = true;
  },

  methods: {
    logout() {
      OpenAPI.TOKEN = undefined;
      this.$cookies.remove("jwt");
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
          <i-button v-if="isLoggedIn" id="logout-button" @click="logout">
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
