<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import Toolbar from "./components/Toolbar.vue"
</script>



<template>
  <q-layout view="hHh lpR fFf">
    <Toolbar/>
    

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

