<template>
  <div class="row items-center absolute-full">
    <LightDarkButton />
    <div class="col-xs-12 col-md-6 flex-center" style="justify-content: center">
      <img v-if="$q.dark.isActive" style="max-width: min(80%, 550px); margin-left: max(10%, (100% - 550px)/2); filter: invert(0.25)"  src="https://osoc.be/img/logo/logo-osoc-color.svg" />
      <img v-else style="max-width: min(80%, 550px); margin-left: max(10%, (100% - 550px)/2)"  src="https://osoc.be/img/logo/logo-osoc-color.svg" />
    </div>
    <div class="col-xs-12 col-md-6">
      <LoginForm />
    </div>
  </div>
</template>

<script lang="ts">
import LoginForm from "./forms/LoginForm.vue";
import LightDarkButton from "./tools/LightDarkButton.vue";

export default {
  components: {LightDarkButton, LoginForm},
}
</script>
