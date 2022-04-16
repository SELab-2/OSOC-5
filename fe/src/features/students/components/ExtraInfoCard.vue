<template>
  <q-card class="full-height cornered">
    <q-card-section>
      <div class="text-h6">
        {{ title }}
      </div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div v-if="studentStore.isLoading">
        <LoadingSpinner />
      </div>

      <div v-else>
        <div v-if="studentStore.currentStudent" style="margin: 0px; padding-left: 0px;">
          {{ content }}
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {useStudentStore} from "../../../stores/useStudentStore";
import LoadingSpinner from "../../../components/LoadingSpinner.vue";
import {defineComponent} from "@vue/runtime-core";

export default defineComponent( {
  components: {LoadingSpinner},
  props: {
    title: {
      type: String,
      required: true
    },
    content: {
      type: String,
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