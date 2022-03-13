<template>
  <img v-if="$q.dark.isActive" src="../../assets/logo_dark.svg"/>
  <img v-else src="../../assets/logo.svg"/>
</template>

<style scoped>
img {
  max-width: min(80%, 550px);
  margin-left: max(10%, (100% - 550px) / 2)
}
</style>