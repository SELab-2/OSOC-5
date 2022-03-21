<template>
  <q-card class="q-ma-sm">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div class="row">
        <div class="col-6">
          The student can work:
          <div v-for="(w, key) in work" :key="key">
            <q-icon v-if="w.present === 'yes'" size="xs" name="mdi-check" color="green"/>
            <q-icon v-else size="xs" name="mdi-close" color="red"/>
            <label class="q-pl-xs">{{ w.description }}</label>
          </div>
        </div>
        <div class="col-6">
          Details:
          <div v-for="(w, key) in details" :key="key">
            <ul style="margin: 0px">
              <li>{{ w.description }}: {{ w.value }}</li>
            </ul>
          </div>
        </div>
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
