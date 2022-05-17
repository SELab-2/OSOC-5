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
        <SuggestionRow :suggestion="decision" />
        <q-separator spaced />
        <div
          v-for="(suggestion, key) in suggestions"
          :key="key"
        >
          <div class="row">
            <SuggestionRow :suggestion="suggestion" />
          </div>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {useStudentStore} from "../../../stores/useStudentStore";
import LoadingSpinner from "../../../components/LoadingSpinner.vue";
import {defineComponent, PropType} from "vue";
import {Suggestion} from "../../../models/Suggestion"
import DecisionIcon from "../../../components/DecisionIcon.vue";
import SuggestionRow from "./SuggestionRow.vue";

export default defineComponent( {
  components: {SuggestionRow, LoadingSpinner},
  props: {
    title: {
      type: String,
        required: true
    },
    suggestions: {
      type: [Object] as PropType<Suggestion[]>,
      required: true
    },
    decision: {
      type: Suggestion,
      required: false,
      default: null
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

<style>
.tooltip-icon {
  left: 2px;
  top: 4px
}
</style>
