<template>
  <div class="fixed-center">
        <Vue3Lottie :animationLink="options[Math.floor(Math.random() * options.length)]" :height="400" :width="400" />
  </div>
</template>

<script lang="ts">

const options = [
  "https://assets8.lottiefiles.com/packages/lf20_GIyuXJ.json",
  "https://assets1.lottiefiles.com/packages/lf20_zyu0ctqb.json",
  "https://assets1.lottiefiles.com/packages/lf20_a3kesdek.json"
]

export default {
  data() {
    return {
      options
    }
  },
}

</script>
