<template>
  <div className="row items-center absolute-full">
    <LightDarkButton/>
    <div className="col-xs-12 col-md-6 flex-center" style="justify-content: center">
      <OsocLogo/>
    </div>
    <div className="col-xs-12 col-md-6 q-pb-md">
      <router-view/>
    </div>
  </div>
</template>

<script lang="ts">
import LightDarkButton from "./components/LightDarkButton.vue";
import OsocLogo from "./components/OsocLogo.vue";

export default {
  components: {OsocLogo, LightDarkButton},
}
</script>