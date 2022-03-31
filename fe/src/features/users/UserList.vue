<template>
  <div class="q-pa-md q-gutter-md">
    <div class="row">
      <div class="text-bold text-h4">
        Users
      </div>
      <q-space />
      <q-btn
        stack
        flat
        color="yellow"
        icon="download"
        label="csv"
        @click="exportTable"
      />
    </div>
    <div class="row q-mb-md vertical-middle">
      <SegmentedControl
        v-model="roleFilter"
        :options="[
          { name: 'all', label: 'All' },
          { name: 'admin', label: 'Admins' },
          { name: 'coach', label: 'Coaches' },
          { name: 'inactive', label: 'Inactive' },
        ]"
      />

      <q-space />
      <q-input
        v-model="filter"
        outlined
        dense
        debounce="300"
        color="yellow-4"
        placeholder="Search"
      >
        <template #append>
          <q-icon name="search" />
        </template>
      </q-input>
    </div>
    
    
    <!-- filter cannot be empty, since this won't trigger the table filter function call.
         This is needed because there are 2 filters, so while the first may not be empty, the second might be. -->
    <q-table
      class="my-table user-table shadow-4"
      :rows="coachStore.users"
      :columns="columns"
      row-key="id"
      :filter="roleFilter"
      :filter-method="useTableFilter"
      separator="horizontal"
    >
      <template #body="props">
        <q-tr
          :class="props.rowIndex % 2 == 1 ? 'bg-yellow-1' : ''"
          :props="props"
        >
          <q-td
            key="name"
            :props="props"
            @click="console.log(props)"
          >
            {{ props.row.firstName }} {{ props.row.lastName }}
          </q-td>
          <q-td
            key="role"
            :props="props"
          >
            <q-select
              v-model="props.row.role"
              v-ripple
              color="yellow"
              borderless
              dense
              style="border-radius: 5px; position: relative; width: 80px"
              :options="roles"
              transition-show="jump-down"
              transition-hide="jump-up"
              transition-duration="300"
              behavior="menu"
              map-options
              emit-value
            >
              <template #option="scope">
                <q-item
                  class="items-center"
                  v-bind="scope.itemProps"
                >
                  <q-icon
                    class="q-mr-md icon"
                    size="xs"
                    :name="scope.opt.icon"
                  />
                  <q-item-section>
                    <q-item-label>{{ scope.opt.label }} </q-item-label>
                  </q-item-section>
                </q-item>
              </template>
            </q-select>
          </q-td>
          <q-td
            key="assignedto"
            :props="props"
          >
            {{ props.row.assignedto }}
          </q-td>
          <q-td
            key="email"
            :props="props"
          >
            {{ props.row.email }}
          </q-td>
          <q-td
            key="remove"
            style="width: 10px"
          >
            <q-btn
              flat
              round
              style="color: #f14a3b"
              icon="mdi-trash-can-outline"
              @click="coachStore.removeUser(props.row.id)"
            />
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from '@vue/runtime-core'
import {useCoachStore} from "../../stores/useCoachStore"
import { ref } from 'vue'
import { exportFile, useQuasar } from 'quasar'
import SegmentedControl from '../../components/SegmentedControl.vue'

const wrapCsvValue = (val: string, formatFn?: ((arg0: unknown) => unknown)|undefined) => {
  let formatted = formatFn !== void 0 ? (formatFn(val) as string) : val

  formatted =
    formatted === void 0 || formatted === null ? '' : String(formatted)

  formatted = formatted.split('"').join('""')
  /**
   * Excel accepts \n and \r in strings, but some other CSV parsers do not
   * Uncomment the next two lines to escape new lines
   */
  // .split('\n').join('\\n')
  // .split('\r').join('\\r')

  return `"${formatted}"`
}

const columns = [
  {
    name: 'name',
    required: true,
    label: 'Name',
    align: 'left',
    field: 'name',
    sortable: true,
  },
  {
    name: 'role',
    required: true,
    label: 'Role',
    align: 'left',
    field: 'role',
    sortable: true,
  },
  {
    name: 'assignedto',
    required: false,
    label: 'Assigned To',
    align: 'left',
    field: 'assignedto',
    sortable: true,
  },
  {
    name: 'email',
    align: 'right',
    label: 'Email',
    field: 'email',
    sortable: true,
  },
  {
    name: 'action',
    align: 'right',
    label: '',
    field: '',
    sortable: false,
  },
]

const roles = [
  {
    label: 'Admin',
    value: 'admin',
    icon: 'mdi-account-outline',
  },
  {
    label: 'Coach',
    value: 'coach',
    icon: 'mdi-whistle-outline',
  },
  {
    label: 'Inactive',
    value: 'inactive',
    icon: 'mdi-close',
  },
]
export default defineComponent({
  components: { SegmentedControl },
  setup() {
    const coachStore = useCoachStore()
    const $q = useQuasar()
    
    onMounted(() => {
      coachStore.loadUsers();
      coachStore.$subscribe((users, state) => {
        console.log(users, state)
        switch (users.events.key) {
            case 'role':
              coachStore
              .updateRole(users.events.target, users.events.newValue)
              .catch((error) => {
                  $q.notify({
                  icon: 'warning',
                  color: 'warning',
                  message: `Error ${error.response.status} while updating role to ${users.events.newValue} for ${users.events.target.firstName} ${users.events.target.lastName}`,
                  textColor: 'black'
                });
                coachStore.users.find((user) => user.id === users.events.target.id).role = users.events.oldValue
              }
            )
        }
      })
    })
    

    return {
      active: ref(true),
      filter: ref(''),
      roleFilter: ref('all'),
      columns,
      roles,
      coachStore,
      $q
    }
  },
  methods: {
    // Method for searching the table.
    // Terms is equal to roleFilter.
    // The method filter to the elements which pass both filters.
    useTableFilter(rows: object[], terms: string, cols: object[], cellValue: (arg0: unknown, arg1: unknown) => string) {
      const lowerTerms = this.filter?.toLowerCase() ?? ''
      
      return rows.filter((row: unknown) =>
        (terms == 'all' || cellValue(cols[1], row) == terms) &&
        cols.some((col: unknown) => {
          const val = cellValue(col, row) + ''
          const haystack =
            val === 'undefined' || val === 'null' ? '' : val.toLowerCase()
          return haystack.indexOf(lowerTerms) !== -1
        })
      )
    },
    exportTable() {
      // naive encoding to csv format
      const current = new Date()
      const cDate =
        current.getFullYear() +
        '' +
        (current.getMonth() + 1) +
        '' +
        current.getDate()
      const cTime =
        current.getHours() + '' + current.getMinutes() + current.getSeconds()
      const dateTime = cDate + '' + cTime
      const content = [
        columns.slice(0, -1).map((col) => wrapCsvValue(col.label)),
      ]
        .concat(
          this.users.map((row: { [x: string]: any }) =>
            columns
              .slice(0, -1)
              .map((col) =>
                wrapCsvValue(
                  typeof col.field === 'function'
                    ? col.field(row)
                    : row[col.field === void 0 ? col.name : col.field],
                  col.format
                )
              )
              .join(',')
          )
        )
        .join('\r\n')

      const status = exportFile(
        'table-export-' + dateTime + '.csv',
        content,
        'text/csv'
      )

      if (status !== true) {
        this.$q.notify({
          message: 'Browser denied file download...',
          color: 'negative',
          icon: 'warning',
        })
      }
    },
  },
})
</script>

<style scoped>
:deep(.q-field__control) {
  border-radius: 10px !important;
}

:deep(.q-btn--rectangle) {
  border-radius: 12px !important;
}

:deep(.q-menu) {
  border-radius: 10px !important;
}

.user-table {
  border-radius: 10px;
}
</style>

<style lang="sass">
.my-table
    thead
        /* bg color is important for th; just specify one */
        background-color: $yellow-7
</style>
