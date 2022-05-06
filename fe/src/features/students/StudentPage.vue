<template>
  <SideBar
    :key="sideBarKey"
    color="bg-grey-3"
    :select-student="selectStudent"
    :draggable="false"
    :must-hover="false"
    @update="update"
  />
  
  <div
    class="fit"
    style=" overflow: auto;"
  >
    <div
      :key="studentKey"
      class="justify-between row q-px-lg q-pt-lg studentcol"
    >
      <div class="row q-px-sm q-gutter-sm items-center">
        <h class="text-bold text-h4">
          {{ student ? student.fullName : '' }}
        </h>
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
          :options="[
            { value: '0', label: 'Yes' },
            { value: '2', label: 'Maybe' },
            { value: '1', label: 'No' },
            { value: '-1', label: 'Not decided' },
          ]"
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
      <q-space />
      <q-btn
        class="cornered"
        outline
        color="red"
        icon-right="delete"
        label="Delete"
        @click="showDeleteDialog"
      />
      <q-dialog v-model="deleteDialog">
        <DeleteStudentDialog
          :name="student?.fullName ?? ''"
          :delete="async () => {
            if (student) {
              await studentStore.deleteStudent(student.url)
              await router.push(`/students`)
            }
          }" 
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
        :options="[
          { name: '0', label: 'Yes' },
          { name: '2', label: 'Maybe' },
          { name: '1', label: 'No' },
          { name: '-1', label: 'Not decided' },
        ]"
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
import DeleteStudentDialog from "./components/DeleteStudentDialog.vue";
import router from "../../router";

export default defineComponent ({
  components: {
    DeleteStudentDialog,
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
      possibleFinalDecision: ref("-1"),
      socket,
      router,
    }
  },
  data() {
    const suggestionDialog = ref(false)
    const deleteDialog = ref(false)
    const reason = ref("")
 
    return {
      sideBarKey: 0,
      studentKey: 0,
      deleteDialog,
      suggestionDialog,
      reason
    }
  },
  computed: {
    student(): Student | null {
      return this.studentStore.currentStudent
    },
    possibleSuggestion(): string {
      return this.studentStore.possibleSuggestion.toString()
    },
    gender(): string {
      let gender = ''
      switch (this.student?.gender) {
        case 0:
          gender += 'Female'
          break
        case 1:
          gender += 'Male'
          break
        case 2:
          gender += 'Transgender'
          break
        default:
          gender += 'Unknown'
          break
      }
      return this.student?.pronouns ? gender + `: ${this.student.pronouns}` : gender
    },
    employment(): string {
      const string = this.student?.employmentAgreement
      return string ? string.charAt(0).toUpperCase() + string.slice(1) : '';
    },
    genderIcon(): string {
      switch (this.student?.gender) {
        case 0:
          return 'mdi-gender-female'
        case 1:
          return 'mdi-gender-male'
        case 2:
          return 'mdi-gender-transgender'
        default:
          return 'person'
      }
    },
    bestSkillColor(): string | null {
      if (this.student) {
        for (const skill of this.student.skills) {
          if (typeof(skill) === 'string') {
            return null
          } else {
            if (skill.name === this.student?.bestSkill) {
              return skill.color
            }
          }
        }
      }
      return null
    },
    mySuggestion(): string {
      if (! this.studentStore.isLoading && this.student) {
        const mySuggestions = this.student.suggestions.filter(suggestion => suggestion.coach.id === this.authenticationStore.loggedInUser?.id)

        return mySuggestions.length > 0 ? mySuggestions[0].suggestion.toString() : (-1).toString()
      } else {
        return this.possibleSuggestion.toString()
      }

    },
    mySuggestionColor(): string {
      let mySuggestion = this.mySuggestion
      switch (mySuggestion) {
        case "0":
          return "green"
        case "1":
          return "red"
        case "2":
          return "yellow"
        default:
          return "grey"
      }
    },
    suggestionName(): string {
      switch (this.possibleSuggestion) {
        case "0":
          return "yes"
        case "1":
          return "no"
        case "2":
          return "maybe"
        default:
          return "not decided"
      }
    },
    suggestionColor(): string {
      switch (this.possibleSuggestion) {
        case "0":
          return "bg-green"
        case "1":
          return "bg-red"
        case "2":
          return "bg-yellow"
        default:
          return "bg-grey"
      }
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
             this.possibleFinalDecision = this.student.finalDecision.suggestion.toString()
          } else if(data.hasOwnProperty('remove_final_decision')) {
            this.studentStore.removeFinalDecision(data.remove_final_decision)

            if(this.student && this.student.finalDecision)
              this.possibleFinalDecision = this.student.finalDecision.suggestion.toString()
          }

          this.update()
      }
   

    // Reload when new student is selected
    this.$watch('id', async (id: number) => {
      await this.studentStore.loadStudent(id)

      if (this.student?.finalDecision) {
        this.possibleFinalDecision = this.student.finalDecision.suggestion.toString()
      } else {
        this.possibleFinalDecision = (-1).toString()
      }
    }, {immediate: true})
  },
  methods: {
    makeSuggestion: async function () {
      if (this.student) {
        await this.studentStore.updateSuggestion(this.student.id, this.reason)
        this.reason = ""
      }

      this.update()
    },
    selectStudent: function (selected_student: Student) {
      this.$router.push(`/students/${selected_student.id}`)
    },
    showDialog: function (value: number) {
      this.studentStore.possibleSuggestion = value
      this.suggestionDialog = true
    },
    showDeleteDialog: function () {
      this.deleteDialog = true
    },
    finalDecision: async function () {
      if (this.student) {
        await this.studentStore.updateFinalDecision(this.student.id, this.possibleFinalDecision)
      }

      this.update()
    },
    update() {
      // Make components update
      this.sideBarKey += 1
      this.studentKey += 1
    }
  },
})
</script>
