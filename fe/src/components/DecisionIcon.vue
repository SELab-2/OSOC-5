<template>
  <q-icon
    class="final-decision-icon"
    size="xs"
    :name="icon"
    :color="color"
  />
</template>

<script lang="ts">
import {Student} from "../models/Student";
import {defineComponent} from "@vue/runtime-core";
import yesMaybeNo from "../models/YesMaybeNo";

export default defineComponent({
  props: {
    student: {
      type: Student,
      required: true
    }
  },
  setup() {
    return {
      yesMaybeNo
    }
  },
  computed: {
    /**
     * Get the final decision suggestion or -1 if there is no final decision
     */
    official(): number {
      if (this.student.finalDecision) {
        return this.student.finalDecision.suggestion
      } else {
        return -1
      }
    },
    icon(): string {
      switch (this.official) {
        case yesMaybeNo.YES.value:
          return yesMaybeNo.YES.icon
        case yesMaybeNo.MAYBE.value:
          return yesMaybeNo.MAYBE.icon
        case yesMaybeNo.NO.value:
          return yesMaybeNo.NO.icon
        default:
          return ''
      }
    },
    color(): string {
      switch (this.official) {
        case yesMaybeNo.YES.value:
          return yesMaybeNo.YES.color
        case yesMaybeNo.MAYBE.value:
          return yesMaybeNo.MAYBE.color
        case yesMaybeNo.NO.value:
          return yesMaybeNo.NO.color
        default:
          return ''
      }
    }
  }
})
</script>

<style scoped>

</style>