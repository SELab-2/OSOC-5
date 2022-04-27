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
        @click="newRolePrompt = true"
        glow-color="#00F1AF"
        shadow-strength=2
      />
      <q-space />
      <q-input
        v-model="filterRoles"
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
            v-if="filterRoles !== ''"
            name="close"
            class="cursor-pointer"
            @click="filterRoles = ''"
          />
          <q-icon
            v-if="filterRoles === ''"
            name="search"
          />
        </template>
      </q-input>
    </div>

    <RoleTable :new-role-prompt="newRolePrompt" />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import RoleTable from "./subcomponents/RoleTable.vue";

export default defineComponent ({
  components: {RoleTable},
  setup() {
    // Filters
    const filterRoles = ref('')

    // variables for the new role dialog popup
    const newRolePrompt = ref(false)

    return {
      newRolePrompt,
      filterRoles,
    }
  },
})
</script>
