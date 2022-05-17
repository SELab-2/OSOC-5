<template>
  <q-table
    v-model:selected="projectStore.selectedCoaches"
    class="table shadow-4"
    :rows="coachStore.users"
    :columns="columnsCoaches"
    :loading="coachStore.isLoading"
    row-key="url"
    selection="multiple"
    :filter="projectStore.filterCoaches"
  >
    <template #body-cell-isAdmin="row">
      <q-td>
        <q-icon
          v-if="row.row.isAdmin === true"
          name="mdi-check"
        />
        <q-icon
          v-else
          name="mdi-close"
        />
      </q-td>
    </template>

    <template #body-cell-isActive="row">
      <q-td>
        <q-icon
          v-if="row.row.isActive === true"
          name="mdi-check"
        />
        <q-icon
          v-else
          name="mdi-close"
        />
      </q-td>
    </template>
  </q-table>
</template>

<script lang="ts">
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
