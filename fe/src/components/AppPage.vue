<template>
  <Toolbar/>
  <router-view/>
</template>

<script lang="ts">
import { defineComponent } from "@vue/runtime-core"
import Toolbar from "./Toolbar.vue"

export default defineComponent({
  components: {Toolbar},
})
</script>

<style scoped>

</style>