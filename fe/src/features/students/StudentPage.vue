<template>
  <div
    class="fit"
    style=" overflow: auto;"
  >
    <div
      class="justify-between row q-px-lg q-pt-lg studentcol"
    >
      <div class="row q-px-sm q-gutter-sm items-center">
        <h class="text-bold text-h4">
          {{ student ? student.fullName : '' }}
        </h>
        <DecisionIcon
          v-if="student?.finalDecison"
          :decision="student.finalDecision.suggestion"
        />
        <q-btn
          :href="student ? student.cv.toString() : ''"
          target="_blank"
          size="12px"
          rounded
          outline
          color="black"
          label="CV"
        />
        <q-btn
          :href="student ? student.portfolio.toString() : ''"
          target="_blank"
          size="12px"
          rounded
          outline
          color="black"
          label="Portfolio"
        />
      </div>
      <div
        v-if="authenticationStore.loggedInUser?.isAdmin ?? false"
        class="row q-gutter-sm items-center"
      >
        <q-select
          v-model="possibleFinalDecision"
          emit-value
          map-options
          rounded
          outlined
          dense
          style="width: 200px"
          :options="yesMaybeNoOptions"
          label="Final decision"
        />
        <q-btn
          class="cornered"
          outline
          label="Confirm"
          @click="decisionDialog = true"
        />
        <q-dialog v-model="decisionDialog">
          <DecisionCard
            :name="student?.fullName ?? ''"
            :suggestion-name="suggestionName(possibleFinalDecision)"
            :suggestion-color="suggestionColor(possibleFinalDecision)"
            :make-suggestion="(reason: string) => finalDecision(reason)"
          />
        </q-dialog>
      </div>
    </div>
    <div class="row q-px-lg q-ml-sm q-mt-sm items-center">
      <InfoDiv
        v-if="student?.alum"
        use-icon="mdi-account-school"
        color="blue"
        title="Alumni"
      />
      <InfoDiv
        v-if="student?.studentCoach"
        use-icon="mdi-account-group"
        color="yellow"
        title="Student coach"
      />
      <InfoDiv
        v-if="student?.employmentAgreement"
        use-icon="mdi-file-document-edit"
        color="red"
        content="Employment"
        :title="employment"
      />
      <InfoDiv
        v-if="student?.gender"
        :use-icon="genderIcon"
        color="green"
        content="Gender"
        :title="gender"
      />
      <q-space />
      <q-btn
        v-if="authenticationStore.loggedInUser?.isAdmin ?? false"
        class="cornered"
        outline
        color="red"
        icon-right="delete"
        label="Delete"
        @click="deleteDialog = true"
      />
      <q-dialog v-model="deleteDialog">
        <DeleteStudentDialog
          :name="student?.fullName ?? ''"
          :delete="deleteStudent"
        />
      </q-dialog>
    </div>

    <div class="row q-px-lg q-ml-sm q-mt-sm items-center">
      <label>Suggest:</label>
    </div>
    <div class="row q-px-lg q-ml-sm items-center">
      <SegmentedControl
        v-model="mySuggestion"
        :color="mySuggestionColor"
        :options="yesMaybeNoOptions"
        @update:modelValue="showDialog"
      />

      <q-dialog v-model="suggestionDialog">
        <DecisionCard
          :name="student?.fullName ?? ''"
          :suggestion-name="suggestionName(studentStore.possibleSuggestion)"
          :suggestion-color="suggestionColor(studentStore.possibleSuggestion)"
          :make-suggestion="(reason: string) => makeSuggestion(reason)"
        />
      </q-dialog>
    </div>

  <div v-if="student" class="q-gutter-sm q-pa-lg">
    <div class="row">
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <SuggestionsCard
          title="Suggestions"
          :suggestions="student?.suggestions"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <AcademiaCard
          :is-loading="studentStore.isLoading"
          :school-name="student?.schoolName"
          :studies="student?.studies"
          :degree="student?.degree"
          :degree-duration="student?.degreeDuration"
          :degree-current-year="student?.degreeCurrentYear"
          title="Academia"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <SkillsCard
          :is-loading="studentStore.isLoading"
          :skills="student?.skills"
          :best-skill="student?.bestSkill"
          title="Skills"
        />
      </div>
    </div>
    <div class="row">
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <LanguageCard
          title="Language"
          :is-loading="studentStore.isLoading"
          :language="student?.language"
          :english-rating="student?.englishRating"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <ExtraInfoCard
          title="Hinder for work"
          :content="student?.hinderWork ?? ''"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <ExtraInfoCard
          title="Fun fact"
          :content="student?.funFact ?? ''"
        />
      </div>
    </div>
    <div class="row">
      <div class="studentcol col-12">
        <ExtraInfoCard
          title="Motivation"
          :content="student?.motivation ?? ''"
        />
      </div>
    </div>
  </div>
  </div>
</template>

<script lang="ts">
import {useAuthenticationStore} from "../../stores/useAuthenticationStore";
import {useStudentStore} from "../../stores/useStudentStore";
import {ref} from "vue";
import AcademiaCard from "./components/AcademiaCard.vue";
import SkillsCard from "./components/SkillsCard.vue";
import SuggestionsCard from "./components/SuggestionsCard.vue";
import SegmentedControl from "../../components/SegmentedControl.vue"
import { Student } from "../../models/Student";
import {defineComponent} from "@vue/runtime-core";
import ExtraInfoCard from "./components/ExtraInfoCard.vue";
import LanguageCard from "./components/LanguageCard.vue";
import DeleteStudentDialog from "./components/DeleteStudentDialog.vue";
import DecisionCard from "./components/DecisionCard.vue";
import InfoDiv from "./components/InfoDiv.vue";
import DecisionIcon from "../../components/DecisionIcon.vue";
import yesMaybeNoOptions from "../../models/YesMaybeNoOptions";
import genderOptions from "../../models/GenderOptions";
import router from "../../router";

export default defineComponent ({
  components: {
    DeleteStudentDialog,
    DecisionCard,
    DecisionIcon,
    InfoDiv,
    LanguageCard,
    ExtraInfoCard,
    AcademiaCard,
    SuggestionsCard,
    SkillsCard,
    SegmentedControl,
  },
  props: {
    id: {
      type: String,
      required: true
    },
  },
  setup() {
    const baseURL =
    process.env.NODE_ENV == 'development'
      ? 'ws://localhost:8000/ws/socket_server/'
      : 'wss://sel2-5.ugent.be/ws/socket_server/'
    const authenticationStore = useAuthenticationStore()
    const studentStore = useStudentStore()
    const socket = new WebSocket(baseURL)

    return {
      authenticationStore,
      studentStore,
      possibleFinalDecision: ref(-1),
      socket,
      yesMaybeNoOptions,
      genderOptions,
      router,
    }
  },
  data() {
    const suggestionDialog = ref(false)
    const decisionDialog = ref(false)
    const deleteDialog = ref(false)
    const reason = ref("")
 
    return {
      deleteDialog,
      suggestionDialog,
      decisionDialog
    }
  },
  computed: {
    /**
     * Retrieve the current selected student from the store
     */
    student(): Student | null {
      return this.studentStore.students.find(s => s.id === parseInt(this.id))
    },
    /**
     * Retrieve the possible suggestion from the store
     */
    gender(): string {
      let gender = genderOptions.find(element => element.value === this.student?.gender)?.name ?? 'Unknown'

      return this.student?.pronouns ? gender + `: ${this.student.pronouns}` : gender
    },
    /**
     * Get the employment agreement of this student
     */
    employment(): string {
      const string = this.student?.employmentAgreement

      // return uppercase agreement or an empty string
      return string ? string.charAt(0).toUpperCase() + string.slice(1) : '';
    },
    /**
     * Get gender icon of this student
     */
    genderIcon(): string {
      return genderOptions.find(element => element.value === this.student?.gender)?.icon ?? 'person'
    },
    /**
     * Get my suggestion if I suggested on this student or if the store is loading, return the possible suggestion
     */
    mySuggestion(): number {
      if (! this.studentStore.isLoading && this.student) {
        const mySuggestions = this.student.suggestions.filter(suggestion => suggestion.coach.id === this.authenticationStore.loggedInUser?.id)

        return mySuggestions.length > 0 ? mySuggestions[0].suggestion : -1
      } else {
        return this.studentStore.possibleSuggestion
      }

    },
    /**
     * Get the color for my suggestion
     */
    mySuggestionColor(): string {
      return yesMaybeNoOptions.find(element => element.value == this.mySuggestion)?.color ?? ''
    },
  },
  mounted() {
      this.socket.onmessage = async (event: { data: string }) => {
          const data = JSON.parse(event.data)

          if(data.hasOwnProperty('suggestion'))
            await this.studentStore.receiveSuggestion(data.suggestion)
          else if(data.hasOwnProperty('remove_suggestion'))
            this.studentStore.removeSuggestion(data.remove_suggestion)
          else if(data.hasOwnProperty('final_decision')) {
            this.studentStore.receiveFinalDecision(data.final_decision)

            if(this.student && this.student.finalDecision)
             this.possibleFinalDecision = this.student.finalDecision.suggestion
          } else if(data.hasOwnProperty('remove_final_decision')) {
            this.studentStore.removeFinalDecision(data.remove_final_decision)

            if(this.student && this.student.finalDecision) {
              this.possibleFinalDecision = this.student.finalDecision.suggestion
            }
          }
      }

    // Reload when new student is selected
    this.$watch('id', async (id: number) => {
      await this.studentStore.loadStudent(id)

      if (this.student?.finalDecision) {
        this.possibleFinalDecision = this.student.finalDecision.suggestion
      } else {
        this.possibleFinalDecision = -1
      }
    }, {immediate: true})
  },
  methods: {
    /**
     * Make a suggestion on this student
     */
    makeSuggestion: async function (reason: string) {
      if (this.student) {
        await this.studentStore.updateSuggestion(this.student.id, reason)
      }

    },
    selectStudent: function (selected_student: Student) {
      this.$router.push(`/students/${selected_student.id}`)
    },
    /**
     * Set possible suggestion and show dialog
     * @param value
     */
    showDialog: function (value: number) {
      this.studentStore.possibleSuggestion = value
      this.suggestionDialog = true
    },
    deleteStudent: async function () {
      if (this.student) {
        await this.studentStore.deleteStudent(this.student.url,
          () => {
            this.$q.notify({
              icon: 'done',
              color: 'positive',
              message: 'Successfully deleted!',
            })
            router.push(`/students`)
          },
          () => this.$q.notify({
            icon: "close",
            color: "negative",
            message: "Failed to delete!"
          }))
      }
    },
    finalDecision: async function (reason: string) {
      if (this.student) {
        await this.studentStore.updateFinalDecision(this.student.id, this.possibleFinalDecision, reason)
      }
    },
    /**
     * Get the name of the possible suggestion
     */
    suggestionName(suggestion: number): string {
      return yesMaybeNoOptions.find(element => element.value == suggestion)?.label ?? ''
    },
    /**
     * Get the background color of the possible suggestion
     */
    suggestionColor(suggestion: number): string {
      return yesMaybeNoOptions.find(element => element.value == suggestion)?.background ?? ''
    }
  },
})
</script>
