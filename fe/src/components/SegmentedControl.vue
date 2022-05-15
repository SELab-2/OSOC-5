<template>
  <q-tabs
    :class="$q.dark.isActive ? 'bg-dark text-white' : 'bg-white text-black'"
    class="shadow-2"
    :indicator-color="color"
    style="border-radius: 10px;"
    v-bind="$attrs"
  >
    <q-tab
      v-for="(option, index) in options"
      :key="index"
      no-caps
      :ripple="false"
      :name="option.name"
      :label="option.label"
    />
  </q-tabs>
</template>


<script lang="ts">
  import { defineComponent, PropType } from 'vue'

  export default defineComponent({
    props: {
      options: {
        type:  [Object] as PropType<{name: string|number, label: string}[]>, 
        required: true
      },
      color: {
        type: String,
        default: "yellow-4"
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
