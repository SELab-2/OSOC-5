<template>
  <q-card class="full-height cornered">
    <q-card-section>
      <div class="text-h6">
        {{ title }}
      </div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div v-if="isLoading">
        <LoadingSpinner />
      </div>

      <div v-else>
        <ul style="margin: 0px; padding-left: 20px;">
          <li>{{ 'Enrolled at: ' + schoolName }}</li>
          <li>{{ 'Studies: ' + studies }}</li>
          <li>{{ 'Degree: ' + degree }}</li>
          <li>{{ 'Duration of degree: ' + degreeDuration }}</li>
          <li>{{ 'Current year of degree: ' + degreeCurrentYear }}</li>
        </ul>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {useStudentStore} from "../../../stores/useStudentStore";
import LoadingSpinner from "../../../components/LoadingSpinner.vue";
import {defineComponent} from "@vue/runtime-core";
import {Student} from "../../../models/Student";

export default defineComponent( {
  components: {LoadingSpinner},
  props: {
    title: {
      type: String,
      required: true
    },
    schoolName: {
      type: String,
      required: true
    },
    studies: {
      type: String,
      required: true
    },
    degree: {
      type: String,
      required: true
    },
    degreeDuration: {
      type: Number,
      required: true
    },
    degreeCurrentYear: {
      type: Number,
      required: true
    },
    isLoading: {
      type: Boolean,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore,
    }
  },
})
</script>