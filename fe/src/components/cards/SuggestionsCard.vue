<template>
  <q-card class="q-ma-sm full-height">
    <q-card-section >
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div class="column">
        <div v-for="(suggestion, key) in suggestions" :key="key">
          <q-icon v-if="suggestion.suggestion === 'yes'" size="xs" name="mdi-check" color="green" />
          <q-icon v-else-if="suggestion.suggestion === 'maybe'" size="xs" name="mdi-help" color="yellow" />
          <q-icon v-else size="xs" name="mdi-close" color="red" />
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
    const suggestions = [
      { name: 'Michiel Leyman', suggestion: 'yes'},
      { name: 'Dayana Stark', suggestion: 'maybe'},
      { name: 'Echo Sierra', suggestion: 'no'}
    ]

    return {
      suggestions
    }
  }
}
</script>