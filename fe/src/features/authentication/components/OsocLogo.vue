<template>
  <img
    v-if="$q.dark.isActive"
    src="../../../assets/logo_dark.svg"
  >
  <img
    v-else
    src="../../../assets/logo.svg"
  >
</template>

<style scoped>
img {
  display: block; 
  margin-left: auto; 
  margin-right: auto; 
  width: 60%; 
  max-height: 250px;
}
</style>
