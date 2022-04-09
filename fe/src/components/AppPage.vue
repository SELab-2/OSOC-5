<template>
  <TopToolbar/>
  <router-view style="height: 100%"/>
</template>

<script lang="ts">
import { defineComponent } from "@vue/runtime-core"
import TopToolbar from "./TopToolbar.vue"

export default defineComponent({
  components: {TopToolbar},
})
</script>

<style scoped>

</style>