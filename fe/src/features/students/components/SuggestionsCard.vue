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

      <div
        v-else
        class="column"
      >
        <div
          v-for="(suggestion, key) in studentStore.currentStudent?.suggestions"
          :key="key"
        >
          <div class="row">
            <DecisionIcon
              v-if="studentStore.currentStudent"
              :decision="suggestion.suggestion"
            />
            <label class="q-pl-xs">
              {{ `${suggestion.coach.firstName} ${suggestion.coach.lastName}` }}
            </label>
            <q-icon
              v-if="suggestion.reason"
              class="tooltip-icon"
              name="mdi-information-outline"
            >
              <q-tooltip
                anchor="center right"
                self="center start"
              >
                {{ suggestion.reason }}
              </q-tooltip>
            </q-icon>
          </div>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {useStudentStore} from "../../../stores/useStudentStore";
import LoadingSpinner from "../../../components/LoadingSpinner.vue";
import {defineComponent} from "@vue/runtime-core";
import DecisionIcon from "../../../components/DecisionIcon.vue";

export default defineComponent( {
  components: {DecisionIcon, LoadingSpinner},
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
})
</script>

<style>
.tooltip-icon {
  left: 2px;
  top: 4px
}
</style>
