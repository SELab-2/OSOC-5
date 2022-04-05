<template>
  <q-card class="full-height cornered">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <div v-for="(w, key) in content" :key="key">
        <ul style="margin: 0px; padding-left: 10px;">
          <li>{{ w }}</li>
        </ul>
      </div>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
export default {
  props: ['title', 'content']
}
</script>