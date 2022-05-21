<template>
  <q-icon
    class="final-decision-icon"
    v-bind="$attrs"
    :name="icon"
    :color="color"
  >
    <q-tooltip
      v-if="reason"
      anchor="center right"
      self="center start"
    >
      {{ reason }}
    </q-tooltip>
  </q-icon>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import yesMaybeNoOptions from "../models/YesMaybeNoOptions";

export default defineComponent({
  props: {
    decision: {
      type: Number,
      required: true
    },
    reason: {
      type: String,
      required: false,
      default: ''
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