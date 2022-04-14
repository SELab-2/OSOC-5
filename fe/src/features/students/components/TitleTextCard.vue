<template>
  <q-card class="full-height cornered">
    <q-card-section >
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      {{ content }}
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";

export default defineComponent( {
  props: {
    title: {
      type: String,
      required: true
    },
    content: {
      type: String,
      required: true
    }
  }
})
</script>
