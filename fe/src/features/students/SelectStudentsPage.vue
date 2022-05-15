<template>
  <div class="placeholder">
    <div class="q-mb-xl">
        <lottie-animation animationLink="https://assets8.lottiefiles.com/packages/lf20_av8ts5jt.json" :height="200" :width="200" />
        <h6 class="text-bold q-mt-none q-mb-xl">Select a student from the sidebar to get started</h6>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import LottieAnimation from '../../components/LottieAnimation.vue'

export default defineComponent({
  // Name is needed so this component is excluded from keep-alive
  name: 'StudentPlaceholder',
  components: { LottieAnimation }
})
</script>

<style>

.placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center 
}

</style>
