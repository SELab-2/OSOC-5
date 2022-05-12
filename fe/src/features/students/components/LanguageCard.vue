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

      <div class="column" v-else>
        <div v-if="languageString" >
          Language: {{ languageString }}
        </div>
        <div>
          English rating:
          <q-icon
            v-for="index in (englishRating ?? 0)"
            :key="index"
            color="yellow"
            name="star"
          />
          <q-icon
            v-for="index in 5 - (englishRating ?? 0)"
            :key="index"
            color="grey"
            name="star"
          />
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
    isLoading: {
      type: Boolean,
      required: true
    },
    language: {
      type: Number,
      required: true
    },
    englishRating: {
      type: Number,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore,
    }
  },
  computed: {
    languageString(): string {
      switch (this.studentStore.currentStudent?.language) {
        case 0:
          return "Dutch"
        case 1:
          return "English"
        case 2:
          return "French"
        case 3:
          return "German"
        default:
          return ''
      }
    }
  }
})
</script>

<style scoped>

</style>
