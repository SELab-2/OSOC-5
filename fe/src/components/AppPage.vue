<template>
  <TopToolbar />
  <SideBar />
  <q-page-container style="height: 100%">
    <router-view v-slot="{ Component }">
      <keep-alive exclude="EditProject">
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </q-page-container>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'
import TopToolbar from './TopToolbar.vue'
import SideBar from './SideBar.vue'

export default defineComponent({
  components: { TopToolbar, SideBar },
})
</script>

<style scoped></style>
