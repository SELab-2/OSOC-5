<template>
  <q-dialog v-model="this.suggestionDialog">
    <q-card>
      <q-card-section>
        <div class="text-h6">{{ this.suggestionName }}</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Perferendis laudantium minus earum totam modi laborum illo, corporis fuga saepe animi aliquam ea enim assumenda ut nulla natus aperiam quis. Iste.
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="Cancel" v-close-popup/>
        <q-btn flat label="Suggest" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  props: ['suggestionDialog', 'suggestion'],
  computed: {
    suggestionName: function () {
      return this.suggestion === 0 ? "Yes" : this.suggestion === 1 ? "Maybe" : "No"
    }
  }
}
</script>

<style scoped>

</style>