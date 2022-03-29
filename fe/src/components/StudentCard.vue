<template>
  <q-card class="my-card full-width full-height">
    <q-card-section rounded>
      <div class="row justify-between">
        <div >
          <label class="text-bold q-pr-xs">{{ name }}</label>
          <!--          <q-icon v-if="official === 'yes'" size="xs" name="mdi-check" color="green" />-->
          <!--          <q-icon v-else-if="official === 'maybe'" size="xs" name="mdi-help" color="yellow" />-->
          <!--          <q-icon v-else size="xs" name="mdi-close" color="red" />-->
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

<script>
export default {
  props: ['student'],
  computed: {
    total() {
      return this.student.suggestions.length
    },
    yesStyle() {
      const widthYes = 100 * this.student.suggestions.filter(sug => sug.suggestion === 0).length / this.total
      return { width: (widthYes + '%')}
    },
    maybeStyle() {
      const widthMaybe = 100 * this.student.suggestions.filter(sug => sug.suggestion === 1).length / this.total
      return { width: (widthMaybe + '%')}
    },
    noStyle() {
      const widthNo = 100 * this.student.suggestions.filter(sug => sug.suggestion === 2).length / this.total
      return { width: (widthNo + '%')}
    },
    name() {
      return this.student.firstName + ' ' + this.student.lastName
    }
  }
}
</script>
