<template>
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
        v-model="officialSuggestion"
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
      color="primary"
      @click="suggestionDialog = true"
      v-model="mySuggestion"
      :options="[
                { name: 0, label: 'Yes' },
                { name: 1, label: 'Maybe' },
                { name: 2, label: 'No' },
                { name: -1, label: 'Not decided' },
              ]"
    />
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
import {useQuasar} from "quasar";
import {ref} from "vue";
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
  },
  props: ['student'],
  setup() {
    const authenticationStore = useAuthenticationStore()
    const studentStore = useStudentStore()
    const $q = useQuasar()

    return {
      suggestionDialog: ref(false),
      authenticationStore,
      studentStore
    }
  },
  methods: {
    makeSuggestion: function (suggestion) {
      this.studentStore.updateSuggestion(this.student.id, suggestion)
    },
    selectStudent: function (selected_student) {
      this.student = selected_student
    },

  },
  computed: {
    name: function () {
      return this.student.firstName + ' ' + this.student.lastName
    },
    mySuggestion: function () {
      const mySuggestions = this.student ? this.student.suggestions.filter(suggestion => suggestion.coach === this.authenticationStore.loggedInUser) : null

      return mySuggestions ? (mySuggestions.length > 0 ? mySuggestions[0].suggestion : -1): null
    }
  }
}
</script>
