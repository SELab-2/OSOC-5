<template>
  <q-card class="full-height cornered">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div v-for="(w, key) in work" :key="key">
        <q-icon v-if="w.present === 'yes'" size="xs" name="mdi-check" color="green"/>
        <q-icon v-else size="xs" name="mdi-close" color="red"/>
        <label class="q-pl-xs">{{ w.description }}</label>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: ['title'],
  setup() {
    const work = [
      {description: 'under a Belgian employment agreement', present: 'yes'},
      {description: 'during the month of July, Monday through Thursday', present: 'no'},
      {description: 'in the Brussels time zone', present: 'yes'},
      {description: 'own their own laptop', present: 'no'}
    ]

    const details = [
      { description: 'First language', value: 'English'},
      { description: 'Level of English', value: '1/5'}
    ]

    return {
      work,
      details
    }
  }
}
</script>
