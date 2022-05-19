<template>
  <div class="fixed-center">
        <lottie-animation animationLink="https://assets8.lottiefiles.com/packages/lf20_GIyuXJ.json" :height="400" :width="400" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import LottieAnimation from './LottieAnimation.vue'

export default defineComponent({
  name: 'NotFound',
  components: { LottieAnimation },
})

</script>
