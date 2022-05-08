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
          v-for="(suggestion, key) in suggestions"
          :key="key"
        >
          <div class="row">
            <q-icon
              v-if="suggestion.suggestion === YES"
              size="xs"
              name="mdi-check"
              color="green"
            />
            <q-icon
              v-else-if="suggestion.suggestion === NO"
              size="xs"
              name="mdi-close"
              color="red"
            />
            <q-icon
              v-else
              size="xs"
              name="mdi-help"
              color="yellow"
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
import {Suggestion} from "../../../models/Suggestion"
export default defineComponent( {
  components: {LoadingSpinner},
  props: {
    title: {
      type: String,
        required: true
    },
    suggestions: {
      type: Array<Suggestion>,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore,
    }
  },
   data: function() {
    return {
      YES : 0,
      NO : 1,
    };
  },
})
</script>

<style>
.tooltip-icon {
  left: 2px;
  top: 4px
}
</style>
