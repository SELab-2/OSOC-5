<template>
  <div
    class="projectcol col-xs-12 col-sm-12 col-md-12 col-lg-5 col-xl-6"
  >
    <div class="text-h4 q-my-md">
      Project Roles
    </div>
    <div class="row">
      <btn
        class="cornered q-mb-sm"
        color="primary"
        icon="add"
        label="Add role"
        @click="newSkillPrompt = true"
        glow-color="#00F1AF"
        shadow-strength=2
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
      <NewRoleDialog
        :new-role-prompt="newSkillPrompt"
        :reset-new-role-prompt="() => newSkillPrompt = false"
      />
    </q-dialog>

    <RoleTable :new-role-prompt="newSkillPrompt" />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import RoleTable from "./subcomponents/RoleTable.vue";
import {useSkillStore} from "../../../stores/useSkillStore";
import NewRoleDialog from "./subcomponents/NewSkillDialog.vue";

export default defineComponent ({
  components: {NewRoleDialog, RoleTable},
  setup() {
    const skillStore = useSkillStore()

    // Filters
    const filterSkills = ref('')

    // variables for the new role dialog popup
    const newSkillPrompt = ref(false)
    const newSkill = ref('')
    const newSkillColor = ref('')

    return {
      skillStore,
      filterSkills,
      newSkillPrompt,
      newSkill,
      newSkillColor,
    }
  },
})
</script>
