<template>
  <Vue3Lottie v-bind="$attrs" :pauseAnimation="playing" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  data() {
    return {
      playing: ref(false),
    }
  },
  // Lottie animation is paused when the view is deactivated.
  // This is done for performance reasons when used in conjunction with keep-alive.
  activated() {
    this.playing = false
  },
  deactivated() {
    this.playing = true
  },
})
</script>
