<template>
  <q-tabs
    :class="`bg-${$q.dark.isActive? 'dark' : 'white'} text-${$q.dark.isActive ? 'white' : 'black'} ${noShadow ? '' : 'shadow-2'}`"
    :indicator-color="color"
    style="border-radius: 10px;"
    :active-class="`text-${invertText ? 'white' : 'black'}`"
    v-bind="$attrs"
  >
    <q-tab
      v-for="(option, index) in options"
      :key="index"
      no-caps
      :style="noPadding ? 'padding: 0px 0px !important;' : ''"
      :ripple="false"
      :name="option.name as any"
      :label="option.label"
    >
    <div v-if="option.amount !== undefined" class="text-caption" color="red" floating>{{ option.amount! }}</div>
    </q-tab>
  </q-tabs>
</template>

<!-- A custom control for selecting one option. 
This component has a different style than the default quasar one, and fits in better with the rest of the website. -->
<script lang="ts">
  import { defineComponent, PropType } from 'vue'

  export default defineComponent({
    props: {
      // The different options that can be chosen.
      options: {
        type:  [Object] as PropType<{name: string|number|boolean, label: string, amount?: number}[]>, 
        required: true
      },
      // Accent color of the component.
      color: {
        type: String,
        default: "yellow"
      },
      // Removes padding around the text of each option. Useful for when there is limited space.
      noPadding: {
        type: Boolean
      },
      // Removed the shadow around the component.
      noShadow: {
        type: Boolean
      },
      // Inverts the text, so the active option has a white color instead of black.
      // Useful when the accent color has a darker shade.
      invertText: {
        type: Boolean
      }
    }
  })
</script>

<style scoped>
  :deep(.q-tab) {
    z-index: 1 !important;
    min-height: 0px !important;
  }
  
  :deep(.fixed-bottom), :deep(.absolute-bottom) {
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    top: auto !important;
  }
  
  :deep(.q-focus-helper) {
    visibility: hidden;
  }
  
  :deep(.q-tab__label, .q-tab__content) {
    z-index: 2 !important;
  }
  
  :deep(.q-tab__indicator) {
    border-radius: 7px;
    height: 85% !important;
    color: "blue" !important;
    z-index: -1 !important;
    width: 92%;
  }
</style>
