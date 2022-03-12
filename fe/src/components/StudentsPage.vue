<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-white text-black" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <OsocLogo />
          </q-avatar>
          Selection Tool
        </q-toolbar-title>

        <q-tabs
            align="justify"
            active-color="green"
            fixed-center
        >
          <q-route-tab to="/students" label="Students" />
          <q-route-tab to="/students" label="Projects" />
          <q-route-tab to="/students" label="Users" />
          <q-route-tab to="/me" icon="mdi-account-circle">
            <label>Miet Claeys</label>
          </q-route-tab>
        </q-tabs>

      </q-toolbar>

    </q-header>

    <SideBar :open="leftDrawerOpen"/>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import OsocLogo from "./tools/OsocLogo.vue";
import { ref } from 'vue'
import SideBar from "./tools/SideBar.vue";

export default {
  setup () {
    const userKinds = [
      { label: 'All'},
      { label: 'Alumni'},
      { label: 'Student Coaches'}
    ]
    const leftDrawerOpen = ref(true)

    return {
      userKind: ref('one'),
      userKinds,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  },
  components: {SideBar, OsocLogo},
}
</script>