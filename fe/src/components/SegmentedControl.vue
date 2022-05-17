<template>
  <q-tabs
    class="bg-white text-black shadow-2"
    :indicator-color="color"
    style="border-radius: 10px;"
    v-bind="$attrs"
  >
    <q-tab
      v-for="(option, index) in options"
      :key="index"
      no-caps
      :style="noPadding ? 'padding: 0px 0px !important;' : ''"
      :ripple="false"
      :name="option.name"
      :label="option.label"
    >
    <div v-if="option.amount !== undefined" class="text-caption" color="red" floating>{{ option.amount! }}</div>
    </q-tab>
  </q-tabs>
</template>


<script lang="ts">
  import { defineComponent, PropType } from 'vue'

  export default defineComponent({
    props: {
      options: {
        type:  [Object] as PropType<{name: string|number, label: string, amount?: number}[]>, 
        required: true
      },
      color: {
        type: String,
        default: "yellow-4"
      },
      noPadding: {
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
