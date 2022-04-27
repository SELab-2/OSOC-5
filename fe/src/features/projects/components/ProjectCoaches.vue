<template>
  <div
    class="projectcol col-xs-12 col-sm-12 col-md-6 col-lg-4 col-xl-3"
  >
    <h4 class="projectsubtitle">
      Project Coaches
    </h4>
    <div class="row">
      <q-input
        v-model="projectStore.filterCoaches"
        class="inputfield q-pb-sm"
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
    <q-table
      v-model:selected="projectStore.selectedCoaches"
      class="table shadow-4"
      :rows="coachStore.users"
      :columns="columnsCoaches"
      :loading="coachStore.isLoadingUsers"
      row-key="url"
      selection="multiple"
      :filter="projectStore.filterCoaches"
    />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useProjectStore} from "../../../stores/useProjectStore";
import {useCoachStore} from "../../../stores/useCoachStore";
import columnsCoaches from "../../../models/ProjectCoachColumns";

export default defineComponent({
  setup() {
    const projectStore = useProjectStore()
    const coachStore = useCoachStore()

    return {
      projectStore,
      coachStore,
      columnsCoaches
    }
  }
})
</script>
