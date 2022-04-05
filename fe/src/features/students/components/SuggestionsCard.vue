<template>
  <q-card class="full-height cornered">
    <q-card-section >
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div v-if="this.studentStore.isLoading">
        <LoadingSpinner />
      </div>

      <div v-else class="column">
        <div v-for="(suggestion, key) in this.studentStore.currentStudent?.suggestions" :key="key">
          <q-icon v-if="suggestion.suggestion === 0" size="xs" name="mdi-check" color="green" />
          <q-icon v-else-if="suggestion.suggestion === 1" size="xs" name="mdi-help" color="yellow" />
          <q-icon v-else size="xs" name="mdi-close" color="red" />
          <label class="q-pl-xs">{{ suggestion.first_name + ' ' + suggestion.last_name }}</label>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {useStudentStore} from "../../../stores/useStudentStore";
import LoadingSpinner from "../../../components/LoadingSpinner.vue";

export default {
  components: {LoadingSpinner},
  props: ['title'],
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore,
    }
  },
}
</script>