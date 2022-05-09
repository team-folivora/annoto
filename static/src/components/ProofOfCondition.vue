<script lang="ts">
import { defineComponent } from "vue";
/**
 * A Dialog for proving to be in the right condition to label data
 */
export default defineComponent({
  props: {
    /**
     * Specifies whether the user is attentive and has finished the training
     */
    isAttentive: { type: Boolean, required: true },
    isTrained: { type: Boolean, required: true },
  },

  emits: ["update:isAttentive", "update:isTrained"],

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
      this.$emit("update:isTrained", true);
    },
  },
});
</script>

<template>
  <el-dialog
    id="proof-of-condition"
    v-model="visible"
    title="Proof of Condition"
    size="lg"
    color="warning"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="false"
  >
    Please read the
    <a
      href="https://github.com/team-folivora/annoto/blob/dev/MANUAL.md"
      target="_blank"
    >
      Manual
    </a>
    before labeling the data.
    <br />
    <br />
    Also, please make sure you feel well and concentrated to label the data. If
    you experience tiredness or lack of concentration, you can continue the
    labeling task later.
    <template #footer>
      <el-row justify="space-between">
        <el-checkbox v-model="checked" class="">
            I am attentive and capable of labeling the data and I have read the
            Manual.
        </el-checkbox>
        <el-button type="success" :disabled="!checked" @click="onSubmit()">
          Confirm
        </el-button>
      </el-row>
    </template>
  </el-dialog>
</template>
