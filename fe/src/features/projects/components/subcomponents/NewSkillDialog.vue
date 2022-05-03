<template>
  <q-card class="create-role-popup">
    <q-card-section>
      <div class="text-h6">
        Create a new skill
      </div>
    </q-card-section>

    <q-card-section class="q-pt-none">
      <q-input
        v-model="newSkill"
        outlined
        autofocus
        class="inputfield"
        label="Role name"
        lazy-rules
        :rules="[
            (val) =>
              (val && val.length > 0) || 'Enter the name of the new skill.',
          ]"
      />
    </q-card-section>
    <q-card-section class="q-pt-none">
      <!--  TODO remove the text input if/when we use the color picker -->
      <q-input
        v-model="newSkillColor"
        outlined
        label="text color"
        class="inputfield"
        type="url"
      />
      <!--  INFO if picker gives conversion issues use-->
      <!--  INFO https://quasar.dev/quasar-utils/color-utils#color-conversion-->
<!--      <q-color-->
<!--        v-model="newSkillColor"-->
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
        label="Add skill"
        @click="newSkillConfirm"
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
    newSkillPrompt: {
      type: Boolean,
      required: true
    },
    resetNewSkillPrompt: {
      type: Function,
      required: true
    }
  },
  setup() {
    const skillStore = useSkillStore()

    // Filters
    const filterRoles = ref('')

    // variables for the new role dialog popup
    const newSkill = ref('')
    const newSkillColor = ref('')

    return {
      skillStore,
      filterRoles,
      newSkill,
      newSkillColor
    }
  },
  methods: {
    newSkillConfirm() {
      // check if the new role value is valid
      if (
        this.newSkill &&
        this.newSkill.length > 0 &&
        this.newSkillColor.length > 0
      ) {
        console.log("test")
        // when valid call the store object and add the skill
        this.skillStore.addSkill(
          this.newSkill,
          this.newSkillColor,

          // callback
          (success: boolean) => {
            if (success) {
              this.$q.notify({
                icon: 'done',
                color: 'positive',
                message: `Added new project skill: ${this.newSkill}.`,
                textColor: 'black',
              })
              this.resetNewSkillPrompt()
              this.newSkill = ''
              this.newSkillColor = ''
            } else {
              this.$q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Failed to add skill!',
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
