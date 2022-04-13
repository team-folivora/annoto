<script lang="ts">
import { defineComponent, render } from "vue";
export default defineComponent({
  props: {
    /**
     * The message that is displayed in the ToastNotification
     */
    message: { type: String, required: true },
    /**
     * The type of appearance the ToastNotification should have
     */
    type: {
      type: String,
      default: "info",
    },
    /**
     * The duration of the ToastNotification in milliseconds
     */
    duration: {
      type: Number,
      default: 3000,
    },
    /**
     * Whether the ToastNotification can be manually closed
     */
    dismissible: {
      type: Boolean,
      default: true,
    },
  },

  data() {
    return {
      isActive: true,
      typeIcons: new Map([
        ["info", "ink-info"],
        ["success", "ink-check"],
        ["warning", "ink-warning"],
        ["danger", "ink-danger"],
      ]),
    };
  },

  computed: {
    icon() {
      return this.typeIcons.get(this.type);
    },
  },

  mounted() {
    // This hides the toast after the specified duration. It gets removed from the DOM by the Toaster Plugin afterwards
    setTimeout(() => {
      this.dismiss();
    }, this.duration);
  },

  methods: {
    dismiss() {
      this.isActive = false;
    },

    destroy() {
      const wrapper = this.$el.parentElement;
      render(null, wrapper);
      document.body.removeChild(wrapper);
    },
  },
});
</script>

<template>
  <Transition appear style="animationDuration" @after-leave="destroy">
    <div v-show="isActive" id="container" class="_position:fixed">
      <i-alert :dismissible="dismissible" :color="type" size="md">
        <template #icon>
          <i-icon :name="icon" />
        </template>
        <p>{{ message }}</p>
      </i-alert>
    </div>
  </Transition>
</template>

<style scoped>
div#container {
  top: 30px;
  min-width: 40%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
}

.v-enter-active {
  animation: fadein 0.5s ease-in-out;
}
.v-leave-active {
  animation: fadein 0.5s ease-in-out reverse;
}

@keyframes fadein {
  from {
    top: 0px;
    opacity: 0;
  }
  to {
    top: 30px;
    opacity: 1;
  }
}
</style>
