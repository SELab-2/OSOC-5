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
        <ul v-if="studentStore.currentStudent" style="margin: 0px; padding-left: 0px;">
          <StudentSkillChip
            v-for="(skill, index) in studentStore.currentStudent.skillList"
            :key="index"
            :color="skill.color"
            :name="skill.name"
          />
        </ul>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import {useStudentStore} from "../../../stores/useStudentStore";
import LoadingSpinner from "../../../components/LoadingSpinner.vue";
import StudentSkillChip from "./StudentSkillChip.vue";

export default {
  components: {StudentSkillChip, LoadingSpinner},
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