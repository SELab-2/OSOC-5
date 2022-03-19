<template>
  <div>
    <SideBar/>
    <div class="justify-between row q-pa-lg">
      <div class="row q-gutter-sm items-center">
        <h class="text-bold text-h4">{{ name }}</h>
        <q-icon size="md" class="content-center" name="mdi-twitter"/>
        <q-icon size="md" name="mdi-linkedin"/>
        <q-icon size="md" name="mdi-github"/>
      </div>
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
    <div class="row q-px-lg">
      <div class="col-4">
        <SuggestionsCard title="Suggestions"/>
      </div>
      <div class="col-4">
        <TitleTextCard title="Academia" content="
          Enrolled at Anderson -Erdman
          Studies: Assurance, Intranet
          Type of degree: Bachelor’s degree
          Years into degree: 5"
        />
      </div>
      <div class="col-4">
        <DocumentsCard title="Experience"/>
      </div>
    </div>
    <div class="row q-px-lg">
      <div class="col-12">
        <TitleTextCard title="Project you're most proud of" content="
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        />
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
import DocumentsCard from "../cards/DocumentsCard.vue";

export default {
  components: {
    DocumentsCard,
    SuggestionsCard,
    TitleTextCard,
    StudentCard,
    SegmentedControl,
    SideBar
  },
  setup() {
    const name = ref("Kelly Cruickshank")
    const officialSuggestion = ref("Not Decided")

    return {
      name,
      officialSuggestion
    }
  }
}
</script>