<template>
  <div
    class="projectcol col-xs-12 col-sm-12 col-md-6 col-lg-3 col-xl-3'"
  >
    <div class="text-h4 q-my-md">
      Basic Info
    </div>
    <q-input
      v-model="projectStore.projectName"
      outlined
      label="Project name"
      lazy-rules
      class="inputfield"
      :rules="[
                (val) =>
                  (val && val.length > 0) ||
                  'Please enter the name of the project.',
              ]"
    />
    <q-input
      v-model="projectStore.projectPartnerName"
      outlined
      label="Partner name"
      lazy-rules
      class="inputfield"
      :rules="[
                (val) =>
                  (val && val.length > 0) ||
                  'Please enter the name of the partner.',
              ]"
    />
    <q-input
      v-model="projectStore.projectLink"
      outlined
      label="Project URL"
      lazy-rules
      class="inputfield"
      :rules="[
                (val) =>
                  (val && val.length > 0) ||
                  'Please enter the URL of the project.',
              ]"
    />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useProjectStore} from "../../../stores/useProjectStore";

export default defineComponent({
  setup() {
    const projectStore = useProjectStore()

    return {
      projectStore,
    }
  }
})
</script>
