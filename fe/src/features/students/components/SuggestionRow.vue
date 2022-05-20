<template>
  <div class="row">
    <DecisionIcon
      :decision="suggestion.suggestion"
    />
    <label class="q-pl-xs">
      {{ suggestion.coach ? `${suggestion.coach.firstName} ${suggestion.coach.lastName}` : 'Deleted user' }}
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
</template>

<script lang="ts">
import {Suggestion} from "../../../models/Suggestion";
import DecisionIcon from "../../../components/DecisionIcon.vue";
import {defineComponent, PropType} from "vue";

export default defineComponent ({
  components: {
    DecisionIcon
  },
  props: {
    suggestion: {
      type: Suggestion,
      required: true
    }
  }
})
</script>

<style scoped>

</style>