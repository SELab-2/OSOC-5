<template>
  <q-chip
    outline
    :color="`${this.color}-4`"
    :class="`bg-${this.color}-1`"
    style="border-width: 1.5px; padding-right: 8px; padding-left: 8px"
  >
    <template v-slot:default>
      <div class="row" style="display: flex; align-items: center">
        <div
          class="text-weight-medium"
          style="color: black; padding-left: 0px"
        >
          {{ this.name }}
        </div>
      </div>
    </template>
  </q-chip>
</template>

<script lang="ts">
export default {
  props: {
    color: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    }
  },
}
</script>