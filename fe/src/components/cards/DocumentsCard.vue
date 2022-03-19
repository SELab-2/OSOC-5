<template>
  <q-card class="q-ma-sm">
    <q-card-section >
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div class="column">
        <div v-for="(suggestion, key) in documents" :key="key">
          <label class="q-pl-xs">{{ suggestion.name }}</label>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: ['title', 'content'],
  setup() {
    const documents = [
      { name: 'CV'},
      { name: 'Portfolio'},
    ]

    return {
      documents
    }
  }
}
</script>
