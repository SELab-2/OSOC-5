<template>
  <div >
    <SideBar/>
    <div class="justify-between row q-px-lg q-pt-lg studentcol full-height">
      <div class="row q-pa-sm q-gutter-sm items-center">
        <h class="text-bold text-h4">{{ name }}</h>
        <q-icon size="md" class="content-center" name="mdi-twitter"/>
        <q-icon size="md" name="mdi-linkedin"/>
        <q-icon size="md" name="mdi-github"/>
        <q-btn size='12px' rounded outline color='black' label="CV" />
        <q-btn size='12px' rounded outline color='black' label='Portfolio' />
      </div>
      <div class="row q-gutter-sm items-center">
        <q-btn size='12px' round outline color='black' icon='mail' />
        <q-select
          rounded
          outlined
          dense
          style="width: 150px"
          v-model="officialSuggestion"
          :options="['Not decided', 'Yes', 'Maybe', 'No']"
          label="Suggestion"
        />
      </div>
    </div>

    <div class="row q-px-lg q-ml-sm items-center">
      <label>Suggestion:</label>
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
          <SuggestionsCard title="Suggestions"/>
        </div>
        <div class="studentcol col-xs-12 col-sm-12 col-md-8 col-lg-8">
          <TitleTextCard title="Academia" content="
            Enrolled at Anderson -Erdman
            Studies: Assurance, Intranet
            Type of degree: Bachelor’s degree
            Years into degree: 5"
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
          <PracticalCard title="Practical" />
        </div>
        <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4" >
          <DetailsCard title="Details" />
        </div>
      </div>
      <div class="row">
        <div class="studentcol col-xs-12 col-sm-12 col-md-6 col-lg-6" >
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
</template>

<script lang="ts">
import {ref} from "vue"
import SideBar from "../tools/SideBar.vue"
import SegmentedControl from "../SegmentedControl.vue";
import StudentCard from "../cards/StudentCard.vue";
import TitleTextCard from "../cards/TitleTextCard.vue";
import SuggestionsCard from "../cards/SuggestionsCard.vue";
import PracticalCard from "../cards/PracticalCard.vue";
import DetailsCard from "../cards/DetailsCard.vue";

export default {
  components: {
    DetailsCard,
    PracticalCard,
    SuggestionsCard,
    TitleTextCard,
    StudentCard,
    SegmentedControl,
    SideBar
  },
  setup() {
    const name = ref("Kelly Cruickshank")
    const officialSuggestion = ref("Not Decided")
    const suggestion = ref('yes')

    return {
      suggestion,
      name,
      officialSuggestion
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