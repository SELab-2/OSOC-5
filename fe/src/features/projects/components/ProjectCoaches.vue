<template>
  <div class="projectcol col-xs-12 col-sm-12 col-md-6 col-lg-6 col-xl-3">
    <div class="text-h4 q-my-md">
      Project Coaches
    </div>
    <CoachTable />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import CoachTable from "./subcomponents/CoachTable.vue";

export default defineComponent({
  components: {CoachTable},
})
</script>
