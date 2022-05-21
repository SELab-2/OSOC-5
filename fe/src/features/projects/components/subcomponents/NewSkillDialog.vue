<template>
  <q-dialog
    v-model="_visible"
    persistent
    
  >
  <q-card class="create-skill-popup column" style="min-width: 400px; align-items: center;
  justify-content: center;">
    <q-card-section>
      <div class="text-h6">
        {{ `${_skill?.id === -1 ? 'New' : 'Edit'} Skill` }}
      </div>
    </q-card-section>

    
      <q-input
        style="width: 90%;"
        v-model="_skill!.name"
        outlined
        autofocus
        class="inputfield"
        label="Skill name"
        lazy-rules
        :rules="[
          (val) => (val && val.length > 0) || 'Enter the name of the skill.',
        ]"
      />
    
    <q-card-section>
      <div class="row" style="max-width: 230px">
        <q-chip
          v-for="color in quasarColors"
          :key="color"
          @click="_skill!.color = color"
          outline
          clickable
          :color="`${color}-${_skill?.color === color ? 8 : 4}`"
          :class="`bg-${color}-${_skill?.color === color ? 4 : 1}`"
          style="border-width: 1.5px;"
        >
        <div 
          v-if="_skill?.color === color" 
          class="bg-white" 
          style="width: 8px; height: 8px; border-radius: 30px; position: absolute; margin-left: auto;margin-right: auto;left: 0;right: 0;"
        />
        </q-chip>

      </div>
    </q-card-section>
    <q-card-actions
      align="right"
      class="text-primary"
    >
      <btn
        v-if="skill?.id !== -1"
        flat
        color="red"
        label="Delete"
        @click="showDelete = true"
      />
      <btn
        v-close-popup
        flat
        label="Cancel"
        glow-color="#C0FFF4"
        @click="_skill!.name = backup!.name; _skill!.color = backup!.color; _visible = false"
      />
      <btn
        v-close-popup
        flat
        :label="_skill?.id === -1 ? 'Add' : 'Update'"
        glow-color="#C0FFF4"
        @click="$emit('submit'); _visible = false"
      />
    </q-card-actions>
  </q-card>
  </q-dialog>
  <DeleteSkillDialog :deleteSkillId="_skill?.id ?? -1" :deleteSkillName="_skill?.name ?? ''" v-model:visible="showDelete"/>
</template>

<script lang="ts">
import { defineComponent, ref, Ref } from '@vue/runtime-core'
import { useSkillStore } from '../../../../stores/useSkillStore'
import quasarColors from '../../../../models/QuasarColors'
import { Skill } from "../../../../models/Skill"
import DeleteSkillDialog from './DeleteSkillDialog.vue'

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
  components: { DeleteSkillDialog },
  emits: ['submit', 'update:skill', 'update:modelValue'],
  data() {
    const backup: Ref<Skill | null> = ref(null)
    return {
      skillStore: useSkillStore(),
      backup,
      quasarColors,
      showDelete: ref(false)
    }
  },
  watch: {
    skill(newValue) {
      this.backup = Object.assign({}, newValue)
    }
  },

  computed: {
    _skill: {
      get(): Skill | null {
        if (this.skill) return this.skill
        this.$emit('update:skill', new Skill('', -1, '', ''))
        return new Skill('', -1, '', '')
      },
      set(n: Skill) {
        this.$emit('update:skill', n)
      }
    },
    _visible: {
      get(): boolean {
        return this.modelValue
      },
      set(n: boolean) {
        this.$emit('update:modelValue', n)
      }
    }
  }
})
</script>
