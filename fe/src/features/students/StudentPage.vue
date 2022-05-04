<template>
  <SideBar
    :key="sideBarKey"
    color="bg-grey-3"
    :clickable="true"
    :draggable="false"
    :must-hover="false"
    @update="update"
  />

  <div :key="studentKey"
    class="justify-between row q-px-lg q-pt-lg studentcol">
    <div class="row q-px-sm q-gutter-sm items-center">
      <h class="text-bold text-h4">
        {{ student ? student.fullName : '' }}
      </h>
      <DecisionIcon v-if="student !== null && student.finalDecision !== null" :decision="student.finalDecision.suggestion" />
      <q-btn :href="student ? student.cv.toString() : ''" target="_blank" size='12px' rounded outline color='black' label="CV"/>
      <q-btn :href="student ? student.portfolio.toString() : ''" target="_blank" size='12px' rounded outline color='black' label='Portfolio'/>
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
        @click="finalDecision"
      />
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
            @click="makeSuggestion"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>

  <div class="q-gutter-sm q-pa-lg">
    <div class="row">
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <SuggestionsCard
          :index="studentKey"
          title="Suggestions"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <AcademiaCard
          :index="studentKey"
          title="Academia"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <SkillsCard
          :index="studentKey"
          title="Skills"
        />
      </div>
    </div>
    <div class="row">
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <LanguageCard
          :index="studentKey"
          title="Language"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <ExtraInfoCard
          :index="studentKey"
          title="Hinder for work"
          :content="studentStore.currentStudent?.hinderWork ?? ''"
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <ExtraInfoCard
          :index="studentKey"
          title="Fun fact"
          :content="studentStore.currentStudent?.funFact ?? ''"
        />
      </div>
    </div>
    <div class="row">
      <div class="studentcol col-12">
        <ExtraInfoCard
          :index="studentKey"
          title="Motivation"
          :content="studentStore.currentStudent?.motivation ?? ''"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {useAuthenticationStore} from "../../stores/useAuthenticationStore";
import {useStudentStore} from "../../stores/useStudentStore";
import {ref} from "vue";
import SideBar from "../../components/SideBar.vue"
import AcademiaCard from "./components/AcademiaCard.vue";
import SkillsCard from "./components/SkillsCard.vue";
import SuggestionsCard from "./components/SuggestionsCard.vue";
import SegmentedControl from "../../components/SegmentedControl.vue"
import { Student } from "../../models/Student";
import {defineComponent} from "@vue/runtime-core";
import ExtraInfoCard from "./components/ExtraInfoCard.vue";
import LanguageCard from "./components/LanguageCard.vue";
import InfoDiv from "./components/InfoDiv.vue";
import DecisionIcon from "../../components/DecisionIcon.vue";
import yesMaybeNoOptions from "../../models/YesMaybeNoOptions";
import genderOptions from "../../models/GenderOptions";

export default defineComponent ({
  components: {
    DecisionIcon,
    InfoDiv,
    LanguageCard,
    ExtraInfoCard,
    AcademiaCard,
    SuggestionsCard,
    SkillsCard,
    SegmentedControl,
    SideBar,
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
      genderOptions
    }
  },
  data() {
    const suggestionDialog = ref(false)
    const reason = ref("")
 
    return {
      sideBarKey: 0,
      studentKey: 0,
      suggestionDialog,
      reason
    }
  },
  computed: {
    /**
     * Retrieve the current selected student from the store
     */
    student(): Student | null {
      return this.studentStore.currentStudent
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
      return yesMaybeNoOptions.find(element => element.value == this.mySuggestion)!.color
    },
    /**
     * Get the name of the possible suggestion
     */
    suggestionName(): string {
      return yesMaybeNoOptions.find(element => element.value == this.studentStore.possibleSuggestion)!.label
    },
    /**
     * Get the background color of the possible suggestion
     */
    suggestionColor(): string {
      return yesMaybeNoOptions.find(element => element.value == this.studentStore.possibleSuggestion)!.background
    }
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

            if(this.student && this.student.finalDecision)
              this.possibleFinalDecision = this.student.finalDecision.suggestion
          }

          this.update()
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
    makeSuggestion: async function () {
      if (this.student) {
        await this.studentStore.updateSuggestion(this.student.id, this.reason)
        this.reason = ""
      }

      this.update()
    },
    /**
     * Set possible suggestion and show dialog
     * @param value
     */
    showDialog: function (value: number) {
      this.studentStore.possibleSuggestion = value
      this.suggestionDialog = true
    },
    /**
     * Make a final decision
     */
    finalDecision: async function () {
      if (this.student) {
        await this.studentStore.updateFinalDecision(this.student.id, this.possibleFinalDecision)
      }

      this.update()
    },
    /**
     * Update components to show new suggestion/decision
     */
    update() {
      // Make components update
      this.sideBarKey += 1
      this.studentKey += 1
    }
  },
})
</script>
