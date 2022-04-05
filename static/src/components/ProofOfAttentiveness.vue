<script lang="ts">
import { defineComponent } from "vue";
/**
 * A Button for annotating a datafile
 */
export default defineComponent({
  data() {
    return {
      visible: true,
      checked: false,
      isAttentive: false,
    };
  },
});
</script>

<template>
  <i-modal
    v-model="visible"
    size="lg"
    color="warning"
    :closeOnPressEscape="false"
    :hideOnClickOutside="false"
    :showClose="false"
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
        <i-button
          @click="
            visible = false;
            isAttentive = true;
            // console.log('Test');
          "
          color="success"
          :disabled="!checked"
        >
          Confirm
        </i-button>
      </div>
    </template>
  </i-modal>
</template>
