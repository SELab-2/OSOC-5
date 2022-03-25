<template>
  <q-icon
      v-if="$q.dark.isActive"
      name="mdi-white-balance-sunny"
      size="2em"
      class="q-ma-md cursor-pointer fixed-top-right"
      @click="$q.dark.toggle"
  />
  <q-icon
      v-else
      name="mdi-moon-waning-crescent"
      size="2em"
      class="q-ma-md cursor-pointer fixed-top-right"
      @click="$q.dark.toggle"
  />
</template>
