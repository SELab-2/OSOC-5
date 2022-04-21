<template>
  <q-layout style="height: 100vh" view="hHh lpR fFf">

    <q-page-container style="height: 100%">
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup lang="ts">
import { useQuasar, QNotifyAction } from 'quasar'

(useQuasar().notify as any).setDefaults({
  position: 'bottom-right',
  actions: [{ icon: 'close', color: 'white' }]
})

</script>

<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

* {
  font-family: 'Montserrat', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

</style>
