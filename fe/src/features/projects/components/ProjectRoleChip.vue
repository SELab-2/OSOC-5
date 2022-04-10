<template>
  <!-- v-model:selected is not used here since this displays an icon, which we don't want. As an alternative, @click is used. -->
  <!-- A Custom implementation of the icon is used, since a chip always reserves place for an icon, even when we don't want it. -->
  <q-chip
    clickable
    @click="enabled = !enabled"
    outline
    :color="`${role.color}-${enabled ? 8 : 4}`"
    :class="`bg-${role.color}-${enabled ? 4 : 1}`"
    :style="`border-width: 1.5px; padding-right: 8px; padding-left: ${role.description ? 2 : 8}px`"
  >
    <template v-slot:default>
      <div class="row" style="display: flex; align-items: center">
        <q-icon
          v-if="role.description"
          name="info"
          size="sm"
          :color="`${role.color}-${enabled ? 2 : 6}`"
        />
        <div
          class="text-weight-medium"
          :style="`color: ${enabled ? 'white' : 'black'}; padding-left: ${role.description ? 3 : 0}px`"
        >
          {{ role.name }}
        </div>
        <div
          class="text-bold"
          style="padding-left: 3px"
          :class="`text-${enabled ? 'white' : `${role.color}-8`}`"
        >
          {{ placesLeft }}
        </div>
        <q-tooltip
          v-if="role.description"
          :class="`bg-${role.color}-2`"
          class="text-black shadow-2"
          anchor="bottom middle"
          self="center middle"
          >{{ role.description }}</q-tooltip
        >
      </div>
    </template>
  </q-chip>
</template>

<script>
import { ref } from 'vue'

export default {
  props: ['role', 'placesLeft', 'modelValue'],
  emits: ['update:modelValue'],
  computed: {
    enabled: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      },
    },
  },
}
</script>
