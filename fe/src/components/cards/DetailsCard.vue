<template>
  <q-card class="full-height">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-md">
      <div v-for="(w, key) in details" :key="key">
        <ul style="margin: 0px; padding-left: 10px;">
          <li>{{ w.description }}: {{ w.value }}</li>
        </ul>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: ['title'],
  setup() {
    const details = [
      { description: 'First language', value: 'English'},
      { description: 'Level of English', value: '1/5'}
    ]

    return {
      details
    }
  }
}
</script>