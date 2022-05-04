<template>
  <q-icon
    class="final-decision-icon"
    size="xs"
    :name="icon"
    :color="color"
  />
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import yesMaybeNoOptions from "../models/YesMaybeNoOptions";

export default defineComponent({
  props: {
    decision: {
      type: Number,
      required: true
    }
  },
  setup() {
    return {
      yesMaybeNoOptions
    }
  },
  computed: {
    icon(): string {
      return yesMaybeNoOptions.find(element => element.value === this.decision)?.icon ?? ''
    },
    color(): string {
      return yesMaybeNoOptions.find(element => element.value === this.decision)?.color ?? ''
    }
  }
})
</script>

<style scoped>

</style>