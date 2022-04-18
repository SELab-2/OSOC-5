<template>
  <div
    class="relative-position container flex justify-center"
    style="width: 100vw"
  >
    <div
      class="q-pa-md q-gutter-md"
      style="width: 1000px"
    >
      <div class="row">
        <div class="text-bold text-h4">
          Sent Mails
        </div>
        <q-space />
        <q-input
          v-model="filter"
          outlined
          dense
          debounce="300"
          color="yellow-4"
          placeholder="Search"
        >
          <template #append>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {ref} from 'vue'

export default defineComponent({
  setup() {
    return {
      filter: ref('')
    }
  }
})
</script>

<style scoped>

</style>