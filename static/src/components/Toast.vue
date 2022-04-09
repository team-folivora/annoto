<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
});
</script>

<template>
  <div :class="{ animate: visible, '_position:fixed': true }" id="container">
    <i-alert dismissible color="success" size="md">
      <template #icon>
        <i-icon name="ink-check" />
      </template>
      <p>Annotation successfully saved</p>
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
