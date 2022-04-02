<template>
  <SideBar :selectStudent="selectStudent" :draggable="false"/>

  <div class="justify-between row q-px-lg q-pt-lg studentcol full-height">
    <div class="row q-pa-sm q-gutter-sm items-center">
      <h class="text-bold text-h4">{{ name }}</h>
      <q-btn :href="this.student.cv" target="_blank" size='12px' rounded outline color='black' label="CV"/>
      <q-btn :href="this.student.portfolio" target="_blank" size='12px' rounded outline color='black' label='Portfolio'/>
    </div>
    <div class="row q-gutter-sm items-center">
      <q-select
        rounded
        outlined
        dense
        style="width: 150px"
        :options="['Not decided', 'Yes', 'Maybe', 'No']"
        label="Final decision"
      />
      <q-btn icon-right="mail" class="cornered" label="Confirm" outline color='black'/>
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
        <SuggestionsCard title="Suggestions" :suggestions="this.student.suggestions"/>
      </div>
      <div class="studentcol col-xs-12 col-sm-12 col-md-8 col-lg-8">
        <AcademiaCard title="Academia" :content="[
              'Enrolled at: ' + this.student.schoolName,
              'Studies: ' + this.student.studies,
              'Degree: ' + this.student.degree
              // 'Years into degree: 5'
            ]"
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

<script>
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

export default {
  components: {
    AcademiaCard,
    DetailsCard,
    PracticalCard,
    SuggestionsCard,
    TitleTextCard,
    SegmentedControl,
    SideBar,
  },
  props: ['id'],
  setup() {
    const authenticationStore = useAuthenticationStore()
    const studentStore = useStudentStore()

    return {
      authenticationStore,
      studentStore,
    }
  },
  data() {
    const possibleSuggestion = ref(null)
    const suggestionDialog = ref(false)
    const reason = ref(null)

    this.studentStore.loadStudent(this.id)

    return {
      possibleSuggestion,
      suggestionDialog,
      reason
    }
  },
  mounted() {
    // Reload when new student is selected
    this.$watch('id', id => {
      this.studentStore.loadStudent(this.id)
    }, {immediate: true})
  },
  methods: {
    makeSuggestion: function (suggestion) {
      this.studentStore.updateSuggestion(this.student.id, this.possibleSuggestion)
    },
    selectStudent: function (selected_student) {
      this.$router.push(`/students/${selected_student.id}`)
    },
    showDialog: function (value) {
      this.possibleSuggestion = value
      this.suggestionDialog = true
    }
  },
  computed: {
    student: function() {
      return this.studentStore.currentStudent
    },
    name: function () {
      return this.student.firstName + ' ' + this.student.lastName
    },
    mySuggestion: function () {
      const mySuggestions = this.student.suggestions.filter(suggestion => suggestion.email === this.authenticationStore.loggedInUser.email)

      return mySuggestions ? (mySuggestions.length > 0 ? mySuggestions[0].suggestion : -1) : null
    },
    mySuggestionColor: function () {
      let mySuggestion = this.mySuggestion
      return mySuggestion === 0 ? "green" : (mySuggestion === 1 ? "yellow" : (mySuggestion === 2 ? "red" : "grey"))
    },
    suggestionName: function () {
      return this.possibleSuggestion === 0 ? "yes" : (this.possibleSuggestion === 1 ? "maybe" : "no")
    },
    suggestionColor: function () {
      return this.possibleSuggestion === 0 ? "bg-green" : (this.possibleSuggestion === 1 ? "bg-yellow" : "bg-red")
    }
  }
}
</script>
