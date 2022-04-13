<template>
  <q-chip
    outline
    :color="color ? color + '-4': 'white'"
    :class="color ? 'bg-' + color + '-1' : 'bg-grey-6'"
    style="border-width: 1.5px; padding-right: 8px; padding-left: 8px"
  >
    {{ info }} {{ color }}
  </q-chip>
</template>

<script>
import {defineComponent} from "@vue/runtime-core";

export default defineComponent ({
  props: {
    info: {
      type: String,
      required: true
    },
    color: {
      type: String,
      required: true
    }
  }
})
</script>
