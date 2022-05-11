<template>
  <div>
    <q-input
      v-model="search"
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
          v-if="search !== ''"
          name="close"
          class="cursor-pointer"
          @click="search = ''"
        />
        <q-icon
          v-if="search === ''"
          name="search"
        />
      </template>
    </q-input>
    <q-table
      v-model:selected="projectStore.selectedCoaches"
      v-model:pagination="pagination"
      class="table shadow-4"
      :rows="coachStore.users"
      :columns="columnsCoaches"
      row-key="url"
      selection="multiple"
      :filter="search"
      :loading="coachStore.isLoading"
      @request="onRequest"
    />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useProjectStore} from "../../../../stores/useProjectStore";
import {useCoachStore} from "../../../../stores/useCoachStore";
import columnsCoaches from "../../../../models/ProjectCoachColumns";
import {ref} from "vue";

export default defineComponent({
  setup() {
    const projectStore = useProjectStore()
    const coachStore = useCoachStore()

    return {
      projectStore,
      coachStore,
      columnsCoaches
    }
  },
  data() {
    const pagination = ref({
      sortBy: 'name',
      descending: false,
      page: 1,
      rowsPerPage: 5,
      rowsNumber: 5 // if getting data from a server
    })

    return {
      pagination,
      search: ref('')
    }
  },
  computed: {
    filters() {
      const filter = {} as {
        search: string
        page_size: number
        page: number
        ordering: string
      }

      filter.search = this.search
      filter.page_size = this.pagination.rowsPerPage
      filter.page = this.pagination.page
      const order = this.pagination.descending ? '-' : '+'
      if (this.pagination.sortBy === 'name') {
        filter.ordering = `${order}first_name,${order}last_name`
      }

      return filter
    }
  },
  async mounted() {
    await this.coachStore.loadUsersCoaches(this.filters, (count: number) => this.pagination.rowsNumber = count)
  },
  methods: {
    async onRequest(props: any) {
      this.pagination = props.pagination
      await this.coachStore.loadUsersCoaches(this.filters, (count: number) => this.pagination.rowsNumber = count)
    },
  }
})
</script>
