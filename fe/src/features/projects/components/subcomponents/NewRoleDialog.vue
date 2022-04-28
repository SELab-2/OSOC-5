<template>
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
<!--      <q-color-->
<!--        v-model="newRoleColor"-->
<!--        no-header-->
<!--        no-footer-->
<!--        class="color-picker"-->
<!--      />-->
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
        v-close-popup
        flat
        label="Add role"
        @click="newRoleConfirm"
        glow-color="#C0FFF4"
      />
    </q-card-actions>
  </q-card>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import {useSkillStore} from "../../../../stores/useSkillStore";

export default defineComponent ({
  props: {
    newRolePrompt: {
      type: Boolean,
      required: true
    },
    resetNewRolePrompt: {
      type: Function,
      required: true
    }
  },
  setup() {
    const skillStore = useSkillStore()

    // Filters
    const filterRoles = ref('')

    // variables for the new role dialog popup
    const newRole = ref('')
    const newRoleColor = ref('')

    return {
      skillStore,
      filterRoles,
      newRole,
      newRoleColor
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
        console.log("test")
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
              this.resetNewRolePrompt()
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
  }
})
</script>
