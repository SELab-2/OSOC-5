<template>
  <div class="row items-center absolute-full">
    <LightDarkButton />
    <div class="col-xs-12 col-md-6 flex-center" style="justify-content: center">
      <OsocLogo />
    </div>
    <div class="col-xs-12 col-md-6 q-pb-md">
      <LoginForm />
    </div>
  </div>
</template>

<script lang="ts">
import LoginForm from "./forms/LoginForm.vue";
import LightDarkButton from "./tools/LightDarkButton.vue";
import OsocLogo from "./tools/OsocLogo.vue";
import { useMeta } from 'quasar';

const metaData = {
  title: 'Index Page',
  meta: {
    themecolor: { name: 'theme-color', content: '#e8fff6'}
  }
}

export default {
  components: {OsocLogo, LightDarkButton, LoginForm},
  setup() {
    useMeta(metaData)
  }
}
</script>
