<template>
  <!-- v-model:selected is not used here since this displays an icon, which we don't want. As an alternative, @click is used. -->
  <!-- A Custom implementation of the icon is used, since a chip always reserves place for an icon, even when we don't want it. -->
  <q-chip
    clickable
    outline
    :color="`${skill.skill.color}-${enabled ? 8 : 4}`"
    :class="`bg-${skill.skill.color}-${enabled ? 4 : 1}`"
    :style="`border-width: 1.5px; padding-right: 8px; padding-left: ${skill.comment ? 2 : 8}px`"
    @click="enabled = !enabled"
  >
    <template #default>
      <div
        class="row"
        style="display: flex; align-items: center"
      >
        <q-icon
          v-if="skill.comment"
          name="info"
          size="sm"
          :color="`${skill.skill.color}-${enabled ? 2 : 6}`"
        />
        <div
          class="text-weight-medium"
          :style="`color: ${enabled ? 'white' : 'black'}; padding-left: ${
            skill.comment ? 3 : 0
          }px`"
        >
          {{ skill.skill.name }}
        </div>
        <div
          class="text-bold"
          style="padding-left: 3px"
          :class="`text-${enabled ? 'white' : `${skill.skill.color}-8`}`"
        >
          {{ occupied ?? 0 }}/{{ skill.amount }}
        </div>
        <q-tooltip
          v-if="skill.comment"
          :class="`bg-${skill.skill.color}-2`"
          class="text-black shadow-2"
          anchor="bottom middle"
          self="center middle"
        >
          {{ skill.comment }}
        </q-tooltip>
      </div>
    </template>
  </q-chip>
</template>


<script lang="ts">
import { defineComponent } from 'vue'
import { ProjectSkill } from '../../../models/Skill'

export default defineComponent({
  props: {
    skill: {
      type: ProjectSkill,
      required: true
    },
    occupied: {
      type: Number,
      required: false
    },
    modelValue: {
      type: Boolean,
      required: false,
    },
  },
  emits: ['update:modelValue'],
  computed: {
    enabled: {
      get() {
        return this.modelValue
      },
      set(value: boolean) {
        this.$emit('update:modelValue', value)
      },
    },
  },
})
</script>
