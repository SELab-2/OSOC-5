<template>
  <div class="full-width relative-position cursor-pointer">
    <span
      class="dot"
      :class="mySuggestionColor"
      style="position: absolute; z-index: -1; top: 50%; left: 5px; transform: translate(-50%, -50%);"
    />
    <q-card
      class="full-width position"
      :class="active? 'bg-teal-1' : ''"
    >
      <q-card-section rounded>
        <div class="row justify-between">
          <div>
            <label class="text-bold q-pr-xs">{{ student.fullName }}</label>
            <DecisionIcon :student="student"/>
            <q-chip
              v-if="student.alum"
              size="8px"
            >
              Alumni
            </q-chip>
          </div>

          <label class="text-bold">{{ total }}</label>
        </div>
        <div
          class="row"
          style="width: 100%; height: 4px"
        >
          <div
            class="bg-red"
            style="height: 4px"
            :style="noStyle"
            label="Test"
          />
          <div
            class="bg-yellow"
            style="height: 4px"
            :style="maybeStyle"
            label="Test"
          />
          <div
            class="bg-green"
            style="height: 4px"
            :style="yesStyle"
            label="Test"
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
import yesMaybeNo from "../models/YesMaybeNo";

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
     * Get the style for the yes part of the bar with yes/maybe/no
     */
    yesStyle(): { width: string } {
      const widthYes = 100 * this.student.suggestions.filter((sug: Suggestion) => sug.suggestion === yesMaybeNo.YES.value).length / this.total
      return { width: (widthYes + '%')}
    },
    /**
     * Get the style for the maybe part of the bar with yes/maybe/no
     */
    maybeStyle(): { width: string } {
      const widthMaybe = 100 * this.student.suggestions.filter((sug: Suggestion) => sug.suggestion === yesMaybeNo.MAYBE.value).length / this.total
      return { width: (widthMaybe + '%')}
    },
    /**
     * Get the style for the no part of the bar with yes/maybe/no
     */
    noStyle(): { width: string } {
      const widthNo = 100 * this.student.suggestions.filter((sug: Suggestion) => sug.suggestion === yesMaybeNo.NO.value).length / this.total
      return { width: (widthNo + '%')}
    },
    /**
     * Get my own suggestion or -1 if I did not do any suggestion yet
     */
    mySuggestion(): number {
      const mySuggestions = this.student.suggestions.filter((suggestion: Suggestion) => {
        if (this.authenticationStore.loggedInUser != null) {
          return suggestion.coach.id === this.authenticationStore.loggedInUser.id
        }
      })

      return mySuggestions.length > 0 ? mySuggestions[0].suggestion : -1
    },
    /**
     * Get the background color for the given suggestion
     */
    mySuggestionColor: function () {
      return this.mySuggestion === yesMaybeNo.YES.value ? "bg-green" : (this.mySuggestion === yesMaybeNo.MAYBE.value ? "bg-yellow" : (this.mySuggestion === yesMaybeNo.NO.value ? "bg-red" : "bg-grey"))
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
