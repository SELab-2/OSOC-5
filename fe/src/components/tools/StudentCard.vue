<template>
  <q-card class="my-card full-width">
    <q-card-section rounded>
      <div class="row justify-between">
        <div >
          <label class="text-bold q-pr-xs">{{ name }}</label>
          <q-icon v-if="official === 'yes'" size="xs" name="mdi-check" color="green" />
          <q-icon v-else-if="official === 'maybe'" size="xs" name="mdi-help" color="yellow" />
          <q-icon v-else size="xs" name="mdi-close" color="red" />
        </div>
        <label class="text-bold">{{ total }}</label>
      </div>
      <div class="row" style="width: 100%; height: 4px">
        <div class="bg-red" style="height: 4px" :style="noStyle" label="Test"/>
        <div class="bg-yellow" style="height: 4px" :style="maybeStyle" label="Test"/>
        <div class="bg-green" style="height: 4px" :style="yesStyle" label="Test"/>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
export default {
  props: ['name', 'yes', 'maybe', 'no', 'official'],
  computed: {
    total() { return this.yes + this.maybe + this.no },
    yesStyle() { return { width: ((100 * this.yes / this.total) + '%')} },
    maybeStyle() { return { width: ((100 * this.maybe / this.total) + '%')} },
    noStyle() { return { width: ((100 * this.no / this.total) + '%')} },
  }
}
</script>

<style scoped>
</style>