<template>
  <q-tabs
    v-model="value"
    class="bg-white text-black shadow-2"
    :indicator-color="color"
    style="border-radius: 10px;"
  >
    <q-tab v-for="(option, index) in options" :key="index" no-caps :ripple="false" :name="option.name" :label="option.label"/>
  </q-tabs>
</template>


<script>
  import { ref, computed } from 'vue'

  export default {
    props: {
      modelValue: String, 
      options: {
        type: [], // [{ name: String, label: String}]
        required: true
      },
      color: {
        type: String,
        default: "yellow-4"
      }
    },
    emits: ['update:modelValue'],
    computed: {
      value: {
        get() {
          return this.modelValue
        },
        set(value) {
          this.$emit('update:modelValue', value)
        }
      }
    }
  }
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
  
  :deep(.q-tab__label), :deep(.q-tabs__content) {
    overflow: visible !important;
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