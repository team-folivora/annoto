<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },

  computed: {
    content() {
      return this.type === "success"
        ? "Annotation successfully saved"
        : "An error occured. Annotation failed.";
    },
    color() {
      return this.type === "success" ? "success" : "danger";
    },
    icon() {
      return this.type === "success" ? "ink-check" : "ink-danger";
    },
  },
});
</script>

<template>
  <div id="container" :class="[{ animate: visible }, '_position:fixed']">
    <i-alert dismissible :color="color" size="md">
      <template #icon>
        <i-icon :name="icon" />
      </template>
      <p>{{ content }}</p>
    </i-alert>
  </div>
</template>

<style scoped>
div#container {
  visibility: hidden;
  top: 30px;
  min-width: 40%;
  left: 50%;
  transform: translate(-50%, 0px);
  z-index: 9999;
}

div.animate {
  visibility: visible !important;
  -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
  animation: fadein 0.5s, fadeout 0.5s 2.5s;
}

@-webkit-keyframes fadein {
  from {
    top: 0;
    opacity: 0;
  }
  to {
    top: 30px;
    opacity: 1;
  }
}

@keyframes fadein {
  from {
    top: 0;
    opacity: 0;
  }
  to {
    top: 30px;
    opacity: 1;
  }
}

@-webkit-keyframes fadeout {
  from {
    top: 30px;
    opacity: 1;
  }
  to {
    top: 0;
    opacity: 0;
  }
}

@keyframes fadeout {
  from {
    top: 30px;
    opacity: 1;
  }
  to {
    top: 0;
    opacity: 0;
  }
}
</style>
