<template>
  <div
    class="projectcol col-xs-12 col-sm-12 col-md-12 col-lg-5 col-xl-6"
  >
    <div class="text-h4 q-my-md">
      Project Skills
    </div>
    <div class="row">
      <btn
        class="cornered q-mb-sm"
        color="primary"
        icon="add"
        label="Add skill"
        shadow-strength="2"
        glow-color="#00F1AF"
        style="color: black !important; font-weight: bold"
        @click="newSkillPrompt = true"
      />
      <q-space />
      <q-input
        v-model="filterSkills"
        style="max-width: 190px"
        outlined
        dense
        debounce="300"
        color="green"
        class="inputfield q-mb-sm"
        placeholder="Search"
        @keydown.enter.prevent=""
      >
        <template #append>
          <q-icon
            v-if="filterSkills !== ''"
            name="close"
            class="cursor-pointer"
            @click="filterSkills = ''"
          />
          <q-icon
            v-if="filterSkills === ''"
            name="search"
          />
        </template>
      </q-input>
    </div>

    <q-dialog
      v-model="newSkillPrompt"
      persistent
    >
      <NewSkillDialog :reset-new-skill-prompt="() => newSkillPrompt = false" />
    </q-dialog>

    <SkillTable :filter-skills="filterSkills" />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import SkillTable from "./subcomponents/SkillTable.vue";
import NewSkillDialog from "./subcomponents/NewSkillDialog.vue";

export default defineComponent ({
  components: {NewSkillDialog, SkillTable},
  setup() {
    // Filters
    const filterSkills = ref('')

    // variables for the new skill dialog popup
    const newSkillPrompt = ref(false)

    return {
      filterSkills,
      newSkillPrompt,
    }
  },
})
</script>
