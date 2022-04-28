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
            <label class="text-bold q-pr-xs">{{ name }}</label>
            <q-icon
              v-if="official === YES"
              class="final-decision-icon"
              size="xs"
              name="mdi-check"
              color="green"
            />
            <q-icon
              v-else-if="official === MAYBE"
              class="final-decision-icon"
              size="xs"
              name="mdi-help"
              color="yellow"
            />
            <q-icon
              v-else-if="official === NO"
              class="final-decision-icon"
              size="xs"
              name="mdi-close"
              color="red"
            />
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

export default defineComponent({
  components: {
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
  data: function() {
    return {
      YES : 0,
      NO : 1,
      MAYBE : 2,
    };
  },
  computed: {
    total(): number {
      return this.student.suggestions.length
    },
    yesStyle(): { width: string } {
      const widthYes = 100 * this.student.suggestions.filter((sug: Suggestion) => sug.suggestion === this.YES).length / this.total
      return { width: (widthYes + '%')}
    },
    maybeStyle(): { width: string } {
      const widthMaybe = 100 * this.student.suggestions.filter((sug: Suggestion) => sug.suggestion === this.MAYBE).length / this.total
      return { width: (widthMaybe + '%')}
    },
    noStyle(): { width: string } {
      const widthNo = 100 * this.student.suggestions.filter((sug: Suggestion) => sug.suggestion === this.NO).length / this.total
      return { width: (widthNo + '%')}
    },
    name(): string {
      return this.student.firstName + ' ' + this.student.lastName
    },
    official(): number {
      if (this.student.finalDecision) {
        return this.student.finalDecision.suggestion
      } else {
        return -1
      }
    },
    mySuggestion(): number | null {
      if (this.student) {
        const mySuggestions = this.student.suggestions.filter((suggestion: Suggestion) => {
          if (this.authenticationStore.loggedInUser != null) {
            return suggestion.coach.id === this.authenticationStore.loggedInUser.id
          }
        })

        return mySuggestions.length > 0 ? mySuggestions[0].suggestion : -1
      } else {
        return null
      }
    },
    mySuggestionColor: function () {
      let mySuggestion = this.mySuggestion
      return mySuggestion === this.YES ? "bg-green" : (mySuggestion === this.MAYBE ? "bg-yellow" : (mySuggestion === this.NO ? "bg-red" : "bg-grey"))
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
