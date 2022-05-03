<template>
  <q-card class="create-skill-popup">
    <q-card-section>
      <div class="text-h6">
        {{ dialogTitle }}
      </div>
    </q-card-section>

    <q-card-section class="q-pt-none">
      <q-input
        v-model="skillStore.popupName"
        outlined
        autofocus
        class="inputfield"
        label="Skill name"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Enter the name of the skill.',
        ]"
      />
    </q-card-section>
    <q-card-section class="q-pt-none">
      <q-select
        v-model="skillStore.popupColor"
        filled
        use-input
        input-debounce="0"
        label="Color picker"
        :options="options"
        style="width: 250px"
        behavior="menu"
        @filter="filterFn"
      >
        <template #option="scope">
          <q-item v-bind="scope.itemProps">
            <div class="row items-center">
              <q-chip
                clickable
                :color="`${scope.opt}-8`"
                :class="`bg-${scope.opt}-4`"
                :style="`height: 25px; width:25px; border-radius: 50%; margin-right: 15px`"
              />
              <q-item-label>{{ scope.opt }}</q-item-label>
            </div>
          </q-item>
        </template>
        <template #no-option>
          <q-item>
            <q-item-section class="text-grey"> No results </q-item-section>
          </q-item>
        </template>
      </q-select>
    </q-card-section>
    <q-card-actions align="right" class="text-primary">
      <btn
        v-close-popup
        flat
        label="Cancel"
        glow-color="#C0FFF4"
        @click="newSkillCancel"
      />
      <btn
        v-close-popup
        flat
        label="Add skill"
        glow-color="#C0FFF4"
        @click="newSkillConfirm"
      />
    </q-card-actions>
  </q-card>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'
import { ref } from 'vue'
import { useSkillStore } from '../../../../stores/useSkillStore'
import quasarColors from '../../../../models/QuasarColors'

export default defineComponent({
  props: {
    dialogTitle: {
      type: String,
      required: true,
    },
  },
  setup() {
    const skillStore = useSkillStore()

    const options = ref(quasarColors)

    return {
      skillStore,

      options,

      quasarColors,

      filterFn(val: string, update: any) {
        if (val === '') {
          update(() => {
            options.value = quasarColors
          })
          return
        } else {
          update(() => {
            const needle = val.toLowerCase()
            options.value = quasarColors.filter(
              (v) => v.toLowerCase().indexOf(needle) > -1
            )
          })
        }
      },
    }
  },
  methods: {
    newSkillConfirm() {
      // when valid call the store object and add the skill
      this.skillStore.addSkill(
        // callback
        (exitCode: number) => {
          switch (exitCode) {
            case 1: {
              this.$q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Failed to add skill!',
              })
              break
            }
            case 2: {
              this.$q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Invalid name/color!',
              })
              break
            }
            default: {
              this.$q.notify({
                icon: 'done',
                color: 'positive',
                message: `Added new project skill: ${this.skillStore.popupName}.`,
                textColor: 'black',
              })
              this.skillStore.popupName = ''
              this.skillStore.popupColor = ''
              this.skillStore.popupID = -1
              break
            }
          }
        }
      )
    },
    newSkillCancel(){
      this.skillStore.popupName = ''
      this.skillStore.popupColor = ''
      this.skillStore.popupID = -1
    }

  },
})
</script>
