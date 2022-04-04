<template>
  <q-route-tab
    style="padding: 0px 0px"
    ref="glowbutton"
  >
    <template #default>
      <btn 
        style="padding: 0px 16px !important; height: 50px !important;"
        disable-click 
        :label="label"
        v-bind="$attrs"
      />
    </template>
  </q-route-tab>
</template>

<script lang="ts">
  import { defineComponent } from 'vue'
  export default defineComponent({
    name: 'tab',
    props: {
      'label': String,
    },
    mounted() {
      const button = this.$refs.glowbutton as any
      button.$el.removeChild(button.$el.children[0])
    }
  })
</script>

<style scoped>
  :deep(.q-ripple) {
    display:none;
  }
  
  :deep(.q-btn--rectangle) {
    border-radius: 0px !important;
  }

  :deep(.q-tab__content) {
    min-width: 50px !important;
    padding: 0px !important;
  }
</style>
