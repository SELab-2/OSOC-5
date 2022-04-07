<template>
  <q-card class="full-height cornered">
    <q-card-section>
      <div class="text-h6">
        {{ title }}
      </div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div v-if="this.studentStore.isLoading">
        <LoadingSpinner />
      </div>

      <div v-else>
        <ul v-if="studentStore.currentStudent" style="margin: 0px; padding-left: 20px;">
          <li>{{ 'Enrolled at: ' + studentStore.currentStudent.schoolName }}</li>
          <li>{{ 'Studies: ' + studentStore.currentStudent.studies }}</li>
          <li>{{ 'Degree: ' + studentStore.currentStudent.degree }}</li>
        </ul>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {useStudentStore} from "../../../stores/useStudentStore";
import LoadingSpinner from "../../../components/LoadingSpinner.vue";

export default {
  components: {LoadingSpinner},
  props: {
    title: {
      type: String,
      required: true
    },
  },
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore,
    }
  },
}
</script>