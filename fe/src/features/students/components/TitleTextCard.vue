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
export default {
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
}
</script>
