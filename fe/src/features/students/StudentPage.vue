<template>
  <SideBar :key="sideBarKey" :student="this.student" :selectStudent="selectStudent" :draggable="false"/>

  <div :key="studentKey"
    class="justify-between row q-px-lg q-pt-lg studentcol full-height">
    <div class="row q-pa-sm q-gutter-sm items-center">
      <h class="text-bold text-h4">{{ name }}</h>
      <q-btn :href="this.student ? this.student.cv : ''" target="_blank" size='12px' rounded outline color='black' label="CV"/>
      <q-btn :href="this.student ? this.student.portfolio : ''" target="_blank" size='12px' rounded outline color='black' label='Portfolio'/>
    </div>
    <div v-if="this.authenticationStore.loggedInUser" class="row q-gutter-sm items-center">
      <q-select
        v-model="possibleFinalDecision"
        emit-value
        map-options
        rounded
        outlined
        dense
        style="width: 200px"
        :options="[
          { value: 0, label: 'Yes' },
          { value: 1, label: 'Maybe' },
          { value: 2, label: 'No' },
          { value: -1, label: 'Not decided' },
        ]"
        label="Final decision"
      />
      <q-btn @click="finalDecision"
             icon-right="mail"
             class="cornered"
             label="Confirm"
             outline
             color='black'/>
    </div>
  </div>

  <div class="row q-px-lg q-ml-sm q-mt-sm items-center">
    <label>Suggest:</label>
  </div>
  <div class="row q-px-lg q-ml-sm items-center">
    <SegmentedControl
      :color="mySuggestionColor"
      @update:modelValue="showDialog"
      v-model="mySuggestion"
      :options="[
        { name: 0, label: 'Yes' },
        { name: 1, label: 'Maybe' },
        { name: 2, label: 'No' },
        { name: -1, label: 'Not decided' },
      ]"
    />

    <q-dialog v-model="this.suggestionDialog" >
      <q-card>
        <q-card-section>
          <div class="text-h6">Suggest
            <q-btn dense rounded class="text-h6" :class="this.suggestionColor">
              {{ this.suggestionName }}
            </q-btn>
            for {{ this.name }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          Why are you making this decision? (optional)
          <q-input
            v-model="reason"
            filled
            type="textarea"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat color="grey" label="Cancel" v-close-popup/>
          <q-btn flat label="Suggest" @click="makeSuggestion" v-close-popup/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>

  <div class="q-gutter-sm q-pa-lg">
    <div class="row">
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <SuggestionsCard :index="studentKey" title="Suggestions"/>
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-8 col-lg-8">
        <AcademiaCard :index="studentKey"
          title="Academia"
        />
      </div>
    </div>
    <div class="row">
      <div class="studentcol col-12">
        <TitleTextCard title="Project you're most proud of" content="
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        />
      </div>
    </div>
    <div class="row">
      <div class="studentcol col-xs-12 col-sm-12 col-md-8 col-lg-8">
        <PracticalCard title="Practical"/>
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
        <DetailsCard title="Details" :content="[
            { description: 'First language', value: 'English'},
            { description: 'Level of English', value: '1/5'}
          ]"/>
      </div>
    </div>
    <div class="row">
      <div class="studentcol col-xs-12 col-sm-12 col-md-6 col-lg-6">
        <TitleTextCard title="Why do you want to participate in osoc?" content="
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        />
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-6 col-lg-6">
        <TitleTextCard title="Why do you think you're a good fit?" content="
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
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
import DetailsCard from "./components/DetailsCard.vue";
import PracticalCard from "./components/PracticalCard.vue";
import SuggestionsCard from "./components/SuggestionsCard.vue";
import TitleTextCard from "./components/TitleTextCard.vue";
import SegmentedControl from "../../components/SegmentedControl.vue"
import { Student } from "../../models/Student";
import {defineComponent} from "@vue/runtime-core";

export default defineComponent ({
  components: {
    AcademiaCard,
    DetailsCard,
    PracticalCard,
    SuggestionsCard,
    TitleTextCard,
    SegmentedControl,
    SideBar,
  },
  props: {
    id: {
      type: Number,
      required: true
    },
  },
  setup() {
    const authenticationStore = useAuthenticationStore()
    const studentStore = useStudentStore()

    return {
      authenticationStore,
      studentStore,
      possibleFinalDecision: ref(-1),
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
    student(): Student | null {
      return this.studentStore.currentStudent
    },
    possibleSuggestion(): number {
      return this.studentStore.possibleSuggestion
    },
    name(): string {
      return this.student ? this.student.firstName + ' ' + this.student.lastName : ""
    },
    mySuggestion(): number | null {
      if (! this.studentStore.isLoading && this.student) {
        const mySuggestions = this.student.suggestions.filter(suggestion => suggestion.coachId === this.authenticationStore.loggedInUser?.pk)

        return mySuggestions.length > 0 ? mySuggestions[0].suggestion : -1
      } else {
        return this.possibleSuggestion
      }

    },
    mySuggestionColor(): string {
      let mySuggestion = this.mySuggestion
      if (mySuggestion !== null) {
        return mySuggestion === 0 ? "green" : (mySuggestion === 1 ? "yellow" : (mySuggestion === 2 ? "red" : "grey"))
      } else {
        return "grey"
      }
    },
    suggestionName(): string {
      switch (this.possibleSuggestion) {
        case 0:
          return "yes"
        case 1:
          return "maybe"
        case 2:
          return "no"
        default:
          return "not decided"
      }
    },
    suggestionColor(): string {
      switch (this.possibleSuggestion) {
        case 0:
          return "bg-green"
        case 1:
          return "bg-yellow"
        case 2:
          return "bg-red"
        default:
          return "bg-grey"
      }
    }
  },
  mounted() {
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
    makeSuggestion: async function () {
      if (this.student) {
        await this.studentStore.updateSuggestion(this.student.id, this.reason)
        this.reason = ""
      }

      // Make components update
      this.sideBarKey += 1
      this.studentKey += 1
    },
    selectStudent: function (selected_student: Student) {
      this.$router.push(`/students/${selected_student.id}`)
    },
    showDialog: function (value: number) {
      this.studentStore.possibleSuggestion = value
      this.suggestionDialog = true
    },
    finalDecision: async function () {
      if (this.student) {
        await this.studentStore.updateFinalDecision(this.student.id, this.possibleFinalDecision)
      }

      // Make components update
      this.sideBarKey += 1
      this.studentKey += 1
    }
  },
})
</script>
