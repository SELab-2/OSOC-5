<template>
  <Toolbar/>
</template>

<script lang="ts">
import Toolbar from "./Toolbar.vue"
import { useQuasar, useMeta } from 'quasar'

const metaData = {
  meta: {
    themecolor: {name: 'theme-color', content: '#24a3cb'}
  }
}

export default {
  title: "test",
  components: {Toolbar},
  setup() {
    useMeta(metaData)
  }
}
</script>