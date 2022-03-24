<template>
  <q-tabs
    v-model="this.value"
    class="bg-white text-black shadow-2"
    :indicator-color="this.color"
    style="border-radius: 10px;"
  >
    <q-tab v-for="(option, index) in this.options" :key="index" no-caps :ripple="false" :name="option.name" :label="option.label"/>
  </q-tabs>
</template>


<script lang="ts">
  import { ref, computed, defineComponent, PropType } from 'vue'
  
  interface Option {
    name: string
    label: string
  }

  export default defineComponent({
    props: {
      modelValue: String, 
      options: {
        type: [Object as PropType<Option>], // [{ name: String, label: String}]
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
        get(): String {
          return this.modelValue
        },
        set(value: String) {
          this.$emit('update:modelValue', value)
        }
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