<template>
  <div class="placeholder">
    <div class="q-mb-xl">
        <Vue3Lottie :animationLink="options[Math.floor(Math.random() * options.length)]" :height="200" :width="200" />
        <h6 class="text-bold q-mt-none q-mb-xl">Select a student from the sidebar to get started</h6>
    </div>
  </div>
</template>

<script>

const options = [
  "https://assets8.lottiefiles.com/packages/lf20_av8ts5jt.json", // Pijl
  "https://assets7.lottiefiles.com/packages/lf20_lodmufpp.json", // Regenboog
  "https://assets4.lottiefiles.com/private_files/lf30_atq8bxjz.json", // Ogen
  "https://assets7.lottiefiles.com/private_files/lf30_w0rzeebl.json", // Confetti
  "https://assets5.lottiefiles.com/packages/lf20_kyusfkfp.json", // Banaan
  "https://assets5.lottiefiles.com/packages/lf20_zkhpkpyc.json", // Tomaat
  "https://assets7.lottiefiles.com/private_files/lf30_cdui7M.json" // Erwten
  
  
]

export default {
  data() {
    return {
      options
    }
  },
}

</script>

<style scoped>

.placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center 
}
</style>
