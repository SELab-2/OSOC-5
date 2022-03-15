<template>
  <div class="row items-center absolute-full">
    <LightDarkButton />
    <div class="col-xs-12 col-md-6 flex-center" style="justify-content: center">
      <OsocLogo />
    </div>
    <div class="col-xs-12 col-md-6 q-pb-md">
      <SignupForm />
    </div>
  </div>
</template>

<script lang="ts">
import LightDarkButton from "./tools/LightDarkButton.vue";
import OsocLogo from "./tools/OsocLogo.vue";
import SignupForm from "./forms/SignupForm.vue";

export default {
  components: {SignupForm, OsocLogo, LightDarkButton},
}
</script>