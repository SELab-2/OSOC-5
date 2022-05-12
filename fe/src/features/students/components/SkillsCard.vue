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
        <ul style="margin: 0px; padding-left: 0px;">
          <StudentSkillChip
            v-for="(skill, index) in skills"
            :key="index"
            :best-skill="bestSkill ?? ''"
            :color="skill.color as string"
            :name="skill.name as string"
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
import {defineComponent, PropType} from "vue";
import {Skill} from "../../../models/Skill"

export default defineComponent( {
  components: {StudentSkillChip, LoadingSpinner},
  props: {
    title: {
      type: String,
      required: true
    },
    isLoading: {
      type: Boolean,
      required: true
    },
    skills: {
      type: [Object] as PropType<Skill[]>,
      required: true
    },
    bestSkill: {
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
