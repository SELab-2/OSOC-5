<template>
  <q-card class="q-ma-sm full-height">
    <q-card-section >
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      {{ content }}
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: ['title', 'content'],
}
</script>
