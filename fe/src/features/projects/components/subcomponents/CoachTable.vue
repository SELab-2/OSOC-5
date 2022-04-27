<template>
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
</template>

<script>
import {defineComponent} from "@vue/runtime-core";
import {useProjectStore} from "../../../../stores/useProjectStore";
import {useCoachStore} from "../../../../stores/useCoachStore";
import columnsCoaches from "../../../../models/ProjectCoachColumns";

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
