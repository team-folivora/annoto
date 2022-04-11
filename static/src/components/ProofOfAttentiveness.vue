<script lang="ts">
import { defineComponent } from "vue";
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  props: {
    /**
     * Specifies whether the user is attentive
     */
    isAttentive: { type: Boolean, required: true },
  },

  emits: ["update:isAttentive"],

  data() {
    return {
      /**
       * Sets the visibility of the modal
       */
      visible: true,
      /**
       * Indicates whether the checkbox in the modal is checked
       */
      checked: false,
    };
  },

  methods: {
    onSubmit() {
      this.visible = false;
      this.$emit("update:isAttentive", true);
    },
  },
});
</script>

<template>
  <i-modal
    v-model="visible"
    size="lg"
    color="warning"
    :close-on-press-escape="false"
    :hide-on-click-outside="false"
    :show-close="false"
  >
    <template #header>
      <p class="h4 _margin:0 _text:center _width:100%">
        Proof of attentiveness
      </p>
    </template>
    Please make sure you feel well and concentrated to label the data. If you
    experience tiredness or lack of concentration, you can continue the labeling
    task later.
    <template #footer>
      <div class="_display:flex _justify-content:space-between _flex-wrap:wrap">
        <i-checkbox v-model="checked" class="_text:wrap _margin-y:1/2">
          <span class="_color:dark _position:relative" style="top: -1px">
            I am attentive and capable of labeling the data.
          </span>
        </i-checkbox>
        <i-button color="success" :disabled="!checked" @click="onSubmit()">
          Confirm
        </i-button>
      </div>
    </template>
  </i-modal>
</template>
