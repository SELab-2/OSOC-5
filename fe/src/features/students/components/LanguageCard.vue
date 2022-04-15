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

      <div class="column" v-else>
        <div>
          Language: {{ language }}
        </div>
        <div>
          English rating:
          <q-icon
            v-for="index in (studentStore.currentStudent?.englishRating ?? 0)"
            :key="index"
            color="yellow"
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
  },
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore,
    }
  },
  computed: {
    language(): string {
      switch (this.studentStore.currentStudent?.language ?? null) {
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