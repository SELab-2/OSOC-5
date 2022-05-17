<template>
  <q-chip
    outline
    :color="`${color}-4`"
    :class="`bg-${color}-1`"
    :style="`border-width: 1.5px; padding-right: 8px; padding-left: ${
      name === bestSkill ? 6 : 8
    }px`"
  >
    <template #default>
      <div
        class="row"
        style="display: flex; align-items: center"
      >
        <q-icon
          v-if="name === bestSkill"
          name="mdi-crown"
        />
        <div
          class="text-weight-medium"
          style="color: black; padding-left: 2px"
        >
          {{ name }}
        </div>
      </div>
    </template>
  </q-chip>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";

export default defineComponent( {
  props: {
    color: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    bestSkill: {
      type: String,
      required: true
    }
  },
})
</script>