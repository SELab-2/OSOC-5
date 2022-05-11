<template>
  <div class="projectcol col-xs-12 col-sm-12 col-md-6 col-lg-6 col-xl-3">
    <div class="text-h4 q-my-md">
      Project Coaches
    </div>
    <div class="row">
      <q-input
        v-model="projectStore.filterCoaches"
        class="inputfield q-mb-sm"
        outlined
        dense
        debounce="300"
        color="green"
        placeholder="Search"
        @keydown.enter.prevent=""
      >
        <template #append>
          <q-icon
            v-if="projectStore.filterCoaches !== ''"
            name="close"
            class="cursor-pointer"
            @click="projectStore.filterCoaches = ''"
          />
          <q-icon
            v-if="projectStore.filterCoaches === ''"
            name="search"
          />
        </template>
      </q-input>
    </div>
    <CoachTable />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useProjectStore} from "../../../stores/useProjectStore";
import CoachTable from "./subcomponents/CoachTable.vue";

export default defineComponent({
  components: {CoachTable},
  setup() {
    const projectStore = useProjectStore()

    return {
      projectStore,
    }
  }
})
</script>
