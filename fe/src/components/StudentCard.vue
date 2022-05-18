<template>
  <div class="full-width relative-position cursor-pointer">
    <span
      class="dot"
      :class="mySuggestionColor"
      style="position: absolute; z-index: -1; top: 50%; left: 5px; transform: translate(-50%, -50%);"
    />
    <q-card
      flat
      class="full-width position"
      :class="active? 'bg-teal-1' : ''"
      v-ripple
      style="max-width: 340px; box-shadow: rgba(0, 0, 0, 0.15) 0px 5px 15px 0px, rgba(0, 0, 0, 0.16) 0px 1px 4px !important;"
    >
      <q-card-section>
        <div class="row no-wrap">
          <label class="text-bold q-pr-xs overflow-hidden" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ student.fullName }}</label>
          <DecisionIcon
            v-if="student !== null && student.finalDecision !== null"
            :decision="student.finalDecision.suggestion"
            :reason="student.finalDecision.reason"
          />
          <q-chip
            v-if="student.alum"
            size="8px"
          >
            Alumni
          </q-chip>
          <q-chip
            v-if="student.studentCoach"
            size="8px"
          >
            Student Coach
          </q-chip>
          <q-space/>
          <label class="text-bold">{{ total }}</label>
        </div>
        <div
          class="row"
          style="width: 100%; height: 4px"
        >
          <div
            class="bg-red"
            style="height: 4px"
            :style="getStyle(1)"
          />
          <div
            class="bg-yellow"
            style="height: 4px"
            :style="getStyle(2)"
          />
          <div
            class="bg-green"
            style="height: 4px"
            :style="getStyle(0)"
          />
        </div>
      </q-card-section>
      <q-tooltip
        v-if="mustHover"
        class="bg-grey-1 shadow-5 cornered"
        max-width="300px"
        anchor="top middle"
        self="bottom middle"
        :offset="[0, 5]"
        :delay="500"
      >
        <StudentSkillChip
          v-for="skill of student.skills"
          :key="typeof(skill) !== 'string' ? skill.id : ''"
          :color="typeof(skill) !== 'string' ? skill.color : ''"
          :name="typeof(skill) !== 'string' ? skill.name : ''"
          :best-skill="student.bestSkill"
        />
      </q-tooltip>
    </q-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/runtime-core"
import {useStudentStore} from "../stores/useStudentStore";
import {useAuthenticationStore} from "../stores/useAuthenticationStore";
import { Suggestion } from "../models/Suggestion";
import {Student} from "../models/Student";
import StudentSkillChip from "../features/students/components/StudentSkillChip.vue";
import DecisionIcon from "./DecisionIcon.vue";
import yesMaybeNoOptions from "../models/YesMaybeNoOptions";

export default defineComponent({
  components: {
    DecisionIcon,
    StudentSkillChip,
  },
  props: {
    student: {
      type: Student,
      required: true
    },
    active: {
      type: Boolean,
      required: true
    },
    mustHover: {
      type: Boolean,
      required: true
    }
  },
  setup() {
    const authenticationStore = useAuthenticationStore()
    const studentStore = useStudentStore()

    return {
      studentStore,
      authenticationStore
    }
  },
  computed: {
    /**
     * Get the total number of suggestions on this student
     */
    total(): number {
      return this.student.suggestions.length
    },
    /**
     * Get my own suggestion or -1 if I did not do any suggestion yet
     */
    mySuggestion(): number {
      const mySuggestions = this.student.suggestions.filter((suggestion: Suggestion) => {
        if (this.authenticationStore.loggedInUser != null) {
          return suggestion.coach ? suggestion.coach.id === this.authenticationStore.loggedInUser.id : false
        }
      })

      return mySuggestions.length > 0 ? mySuggestions[0].suggestion : -1
    },
    /**
     * Get the background color for the given suggestion
     */
    mySuggestionColor: function () {
      return yesMaybeNoOptions.find(element => element.value === this.mySuggestion)?.background
    },
  },
  methods: {
    /**
     * Get the width for a div depending on suggestion
     * @param value of suggestion
     */
    getStyle(value: number): { width: string } {
      const width = 100 * this.student.suggestions.filter((sug: Suggestion) => sug.suggestion === value).length / this.total

      return { width: (width + '%')}
    },
  }
})
</script>

<style>
.dot {
  height: 40px;
  width: 20px;
  background-color: #bbb;
  border-radius: 15%;
  display: inline-block;
}
.final-decision-icon {
  top: -2px
}
</style>
