<template>
  <div>
    <SideBar :selectStudent="selectStudent"/>
    <div v-if="!this.student" class="q-pa-lg full-height flex-center">
      <label>Select a student from the sidebar to get started</label>
    </div>

    <div v-if="this.student">
      <div class="justify-between row q-px-lg q-pt-lg studentcol full-height">
        <div class="row q-pa-sm q-gutter-sm items-center">
          <h class="text-bold text-h4">{{ name }}</h>
          <q-icon size="md" class="content-center" name="mdi-twitter"/>
          <q-icon size="md" name="mdi-linkedin"/>
          <q-icon size="md" name="mdi-github"/>
          <q-btn :href="this.student.cv" target="_blank" size='12px' rounded outline color='black' label="CV"/>
          <q-btn :href="this.student.portfolio" target="_blank" size='12px' rounded outline color='black' label='Portfolio'/>
        </div>
        <div class="row q-gutter-sm items-center">
          <q-btn size='12px' round outline color='black' icon='mail'/>
          <q-select
            rounded
            outlined
            dense
            style="width: 150px"
            v-model="officialSuggestion"
            :options="['Not decided', 'Yes', 'Maybe', 'No']"
            label="Final decision"
          />
        </div>
      </div>

      <div class="row q-px-lg q-ml-sm q-mt-sm items-center">
        <label>Suggest:</label>
      </div>
      <div class="row q-px-lg q-ml-sm items-center">
        <SegmentedControl
          color="primary"
          v-model="suggestion"
          :options="[
                { name: 'yes', label: 'Yes' },
                { name: 'maybe', label: 'Maybe' },
                { name: 'no', label: 'No' },
                { name: 'none', label: 'None' },
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
    </div>
  </div>
</template>

<script lang="ts">
import {ref} from "vue"
import { openURL } from 'quasar'
import SideBar from "../tools/SideBar.vue"
import SegmentedControl from "../SegmentedControl.vue";
import StudentCard from "../cards/StudentCard.vue";
import TitleTextCard from "../cards/TitleTextCard.vue";
import SuggestionsCard from "../cards/SuggestionsCard.vue";
import PracticalCard from "../cards/PracticalCard.vue";
import DetailsCard from "../cards/DetailsCard.vue";
import AcademiaCard from "../cards/AcademiaCard.vue";

export default {
  components: {
    AcademiaCard,
    DetailsCard,
    PracticalCard,
    SuggestionsCard,
    TitleTextCard,
    StudentCard,
    SegmentedControl,
    SideBar,
    openURL
  },
  data() {
    const student = ref(null)

    function selectStudent(selected_student) {
      console.log(selected_student)
      student.value = selected_student
    }

    return {
      student, selectStudent
    }
  },
  computed: {
    name: function () {
      console.log(this.student)
      return this.student.firstName + ' ' + this.student.lastName
    }
  }
}
</script>

<style>
.minimum_width {
  min-width: 300px !important;
}

.studentcol {
  padding: 5px;
}

.cornered {
  border-radius: 10px !important
}
</style>