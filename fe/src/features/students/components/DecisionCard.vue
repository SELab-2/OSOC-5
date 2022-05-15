<template>
  <q-card>
    <q-card-section>
      <div class="text-h6">
        Suggest
        <btn
          :label="suggestionName"
          dense
          rounded
          class="text-h6"
          :class="suggestionColor"
        />
        for {{ name }}
      </div>
    </q-card-section>

    <q-card-section class="q-pt-none">
      Why are you making this decision? (optional)
      <q-input
        v-model="reason"
        filled
        type="textarea"
      />
    </q-card-section>

    <q-card-actions
      align="right"
      class="text-primary"
    >
      <btn
        v-close-popup
        flat
        color="grey"
        label="Cancel"
        glow-color="grey-4"
      />
      <btn
        v-close-popup
        flat
        label="Suggest"
        glow-color="teal-1"
        @click="() => makeSuggestion(reason)"
      />
    </q-card-actions>
  </q-card>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {ref} from "vue";

export default defineComponent ({
  props: {
    name: {
      type: String,
      required: true,
    },
    suggestionName: {
      type: String,
      required: true
    },
    suggestionColor: {
      type: String,
      required: true
    },
    makeSuggestion: {
      type: Function,
      required: true
    }
  },
  data() {
    const reason = ref("")

    return {
      reason
    }
  }
})
</script>

<style scoped>

</style>