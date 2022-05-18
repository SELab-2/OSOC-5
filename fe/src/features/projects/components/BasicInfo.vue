<template>
  <div class="variable">
    <div class="text-h4 q-my-md">Basic Info</div>
    <q-input
      v-model="_name"
      outlined
      color="teal"
      label="Project name"
      lazy-rules
      :rules="[
        (val) => (val && val.length > 0) || 'Provide the name of the project.',
      ]"
    />
    <q-input
      v-model="_partnerName"
      outlined
      color="teal"
      label="Partner name"
      lazy-rules
      :rules="[
        (val) => (val && val.length > 0) || 'Provide the name of the partner.',
      ]"
    />
    <q-input
      v-model="_info"
      outlined
      color="teal"
      label="Project Info"
      type="textarea"
      hint="Supports markdown"
    >
    </q-input>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'
import { useProjectStore } from '../../../stores/useProjectStore'

export default defineComponent({
  props: {
    name: {
      type: String,
      required: true,
    },
    partnerName: {
      type: String,
      required: true,
    },
    info: {
      type: String,
      required: true,
    },
  },
  computed: {
    _name: {
      get(): string {
        return this.name
      },
      set(n: string) {
        this.$emit('update:name', n)
      },
    },
    _partnerName: {
      get(): string {
        return this.partnerName
      },
      set(n: string) {
        this.$emit('update:partnerName', n)
      },
    },
    _info: {
      get(): string {
        return this.info
      },
      set(n: string) {
        this.$emit('update:info', n)
      },
    },
  },
})
</script>

<style scoped>
@media only screen and (min-width: 800px) {
  .variable {
    margin: auto;
    width: 80%;
    max-width: 600px;
  }
}
</style>
