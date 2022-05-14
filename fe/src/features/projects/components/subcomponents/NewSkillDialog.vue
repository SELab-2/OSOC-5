<template>
  <q-dialog
    v-model="_visible"
    persistent
  >
  <q-card class="create-skill-popup">
    <q-card-section>
      <div class="text-h6">
        {{ `${_skill.id === -1 ? 'New' : 'Edit'} Skill`  }}
      </div>
    </q-card-section>

    <q-card-section class="q-pt-none">
      <q-input
        v-model="_skill.name"
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
    <q-card-section>
      <div class="row">
        <q-chip
          v-for="color in quasarColors"
          :key="color"
          @click="_skill.color = color"
          clickable
          :color="`${color}-8`"
          :class="`bg-${color}-4`"
          :style="`height: 25px; width:25px; border-radius: 50%; margin-right: 15px`"
        />
      </div>
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
        @click="() => { _skill = backup; _visible = false }"
      />
      <btn
        v-close-popup
        flat
        :label="_skill.id === -1 ? 'Add' : 'Update'"
        glow-color="#C0FFF4"
        @click="_visible = false"
      />
    </q-card-actions>
  </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'
import { useSkillStore } from '../../../../stores/useSkillStore'
import quasarColors from '../../../../models/QuasarColors'
import { Skill } from "../../../../models/Skill"

export default defineComponent({
  props: {
    skill: {
      type: Skill,
      required: false
    },
    modelValue: {
      type: Boolean,
      required: true
    }
  },
  data(props) {
    return {
      skillStore: useSkillStore(),
      backup: props.skill,
      quasarColors,
    }
  },
  computed: {
    _skill: {
      get(): Skill | null {
        if (this.skill) return this.skill
        this.$emit('update:skill', new Skill('', -1, '', ''))
        return new Skill('', -1, '', '') // New skill that will removed directly after
      },
      set(n) {
        this.$emit('update:skill', n)
      }
    },
    _visible: {
      get() {
        return this.modelValue
      },
      set(n) {
        this.$emit('update:modelValue', n)
      }
    }
  }
})
</script>
