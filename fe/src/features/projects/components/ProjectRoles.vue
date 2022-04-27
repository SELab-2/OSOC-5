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

    <q-dialog
      v-model="newRolePrompt"
      persistent
    >
      <q-card class="create-role-popup">
        <q-card-section>
          <div class="text-h6">
            Create a new role
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            v-model="newRole"
            outlined
            autofocus
            class="inputfield"
            label="Role name"
            lazy-rules
            :rules="[
            (val) =>
              (val && val.length > 0) || 'Enter the name of the new role.',
          ]"
          />
        </q-card-section>
        <q-card-section class="q-pt-none">
          <!--        TODO REMOVE -->
          <q-input
            v-model="newRoleColor"
            outlined
            label="text color"
            class="inputfield"
            type="url"
          />
          <!--  INFO if picker gives conversion issues use-->
          <!--  INFO https://quasar.dev/quasar-utils/color-utils#color-conversion-->
          <q-color
            v-model="newRoleColor"
            no-header
            no-footer
            class="color-picker"
          />
        </q-card-section>
        <q-card-actions
          align="right"
          class="text-primary"
        >
          <btn
            v-close-popup
            flat
            label="Cancel"
            glow-color="#C0FFF4"
          />
          <btn
            flat
            label="Add role"
            @click="newRoleConfirm"
            glow-color="#C0FFF4"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <RoleTable :new-role-prompt="newRolePrompt" />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import RoleTable from "./subcomponents/RoleTable.vue";
import {useSkillStore} from "../../../stores/useSkillStore";

export default defineComponent ({
  components: {RoleTable},
  setup() {
    const skillStore = useSkillStore()

    // Filters
    const filterRoles = ref('')

    // variables for the new role dialog popup
    const newRolePrompt = ref(false)
    const newRole = ref('')
    const newRoleColor = ref('')

    // Role amount error handling
    const errorRoleAmount = ref(false)
    const errorMessageRoleAmount = ref('')

    return {
      skillStore,
      filterRoles,
      newRolePrompt,
      newRole,
      newRoleColor,
      errorRoleAmount,
      errorMessageRoleAmount
    }
  },
  methods: {
    newRoleConfirm() {
      // check if the new role value is valid
      if (
        this.newRole &&
        this.newRole.length > 0 &&
        this.newRoleColor.length > 0
      ) {

        // when valid call the store object and add the skill
        this.skillStore.addSkill(
          this.newRole,
          this.newRoleColor,

          // callback
          (success: boolean) => {
            if (success) {
              this.$q.notify({
                icon: 'done',
                color: 'positive',
                message: `Added new project role: ${this.newRole}.`,
                textColor: 'black',
              })
              this.newRolePrompt = false
              this.newRole = ''
              this.newRoleColor = ''
            } else {
              this.$q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Failed to add role!',
              })
            }
          }
        )
      } else {
        this.$q.notify({
          icon: 'close',
          color: 'negative',
          message: 'Invalid name/color!',
        })
      }
    },
    amountRangeValidation(val: number) {
      if (val < 0) {
        this.errorRoleAmount = true
        this.errorMessageRoleAmount = 'The value must be positive!'
        return false
      }
      this.errorRoleAmount = false
      this.errorMessageRoleAmount = ''
      return true
    },
  }
})
</script>
