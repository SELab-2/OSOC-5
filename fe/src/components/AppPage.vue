<template>
  <TopToolbar />
  <SideBar />
  <q-page-container style="height: 100%; overflow: auto">
    <router-view v-slot="{ Component }">
      <!-- KeepAlive is used so the major views are cached, which simplifies lots of things, and more state is kept when switching tabs. -->
      <keep-alive exclude="CreateProject,StudentPlaceholder,NotFound">
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
