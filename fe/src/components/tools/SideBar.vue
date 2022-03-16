<template>
  <q-drawer side="left" bordered show-if-above>
    <div class="q-pa-md">
      <label class="q-pa-md">Students</label>
      <q-input icon="mdi-search" class="q-ma-md" clearable filled v-model="search" label="Search..." />
      <q-btn-toggle
          size="md"
          v-model="userKind"
          spread
          no-caps
          toggle-color="green"
          color="white"
          text-color="black"
          class="q-ma-md"
          :options="userKinds"
      />
      <q-btn-toggle
          size="md"
          v-model="suggestion"
          spread
          no-caps
          toggle-color="green"
          color="white"
          text-color="black"
          class="q-ma-md"
          :options="suggestionKinds"
      />
      <q-select class="q-ma-md" filled v-model="model" :options="options" label="Filled" />
    </div>

  </q-drawer>
</template>

<script>
import { ref } from 'vue'
export default {
  setup () {
    const userKinds = [
      {label: 'All', value: 'All'},
      {label: 'Alumni', value: 'Alumni'},
      {label: 'Student Coaches', value: 'Student Coaches'}
    ]
    const suggestionKinds = [
      {label: 'Yes', value: 'Yes'},
      {label: 'Maybe', value: 'Maybe'},
      {label: 'No', value: 'No'},
      {label: 'None', value: 'None'}
    ]
    return {
      search: ref(""),
      userKind: ref('All'),
      suggestion: ref('None'),
      userKinds,
      suggestionKinds
    }
  }
}
</script>