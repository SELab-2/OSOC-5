<template>
  <div
    class="projectcol col-xs-12 col-sm-12 col-md-12 col-lg-12 col-xl-6"
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
        @click="openDialog"
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
      <NewSkillDialog
        dialog-title="Create a new skill"
        submit-text="Add skill"
        :callback="() => newSkillPrompt = false"
      />
    </q-dialog>

    <SkillTable :filter-skills="filterSkills" />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import SkillTable from "./subcomponents/SkillTable.vue";
import NewSkillDialog from "./subcomponents/NewSkillDialog.vue";
import { useSkillStore } from "../../../stores/useSkillStore";

export default defineComponent ({
  components: {NewSkillDialog, SkillTable},
  setup() {

    const skillStore = useSkillStore()

    // Filters
    const filterSkills = ref('')

    // variables for the new skill dialog popup
    const newSkillPrompt = ref(false)

    return {
      skillStore,
      filterSkills,
      newSkillPrompt,

      openDialog(){
        newSkillPrompt.value = true;
        skillStore.popupName = ''
        skillStore.popupColor = ''
        skillStore.popupID = -1

      },
    }
  },
})
</script>
