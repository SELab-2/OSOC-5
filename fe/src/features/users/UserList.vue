<template>
  <div
    class="relative-position container flex justify-center"
    style="width: 100vw"
  >
    <div
      class="q-pa-md q-gutter-md"
      style="width: 1000px"
    >
      <div class="row">
        <div class="text-bold text-h4">
          Users
        </div>
        <q-space />
        <btn
          stack
          flat
          color="yellow"
          icon="download"
          label="csv"
          glow-color="amber-2"
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
        <div class="row q-px-sm">
          <btn color="yellow" icon-right="add" class="text-black" label="Add User" @click="newUserDialog = true" shadow-color="orange" shadow-strength="2"/>
        </div>
        <div class="row q-px-sm">
          <q-space/>
          <q-dialog v-model="newUserDialog">
            <q-card>
              <AddUser />
            </q-card>
          </q-dialog>
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
      </div>

      <!-- filter cannot be empty, since this won't trigger the table filter function call.
             This is needed because there are 2 filters, so while the first may not be empty, the second might be. -->
      <q-table
        class="my-table user-table shadow-4"
        table-header-style="user-table"
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
            >
              {{ props.row.fullName }}
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
                    @click="() => updateRole(props.row, props.row.role)"
                    class="items-center"
                    v-bind="scope.itemProps"
                  >
                    <q-icon
                      class="q-mr-md icon"
                      size="xs"
                      :name="scope.opt.icon"
                    />
                    <q-item-section>
                      <q-item-label>{{ scope.opt.label }}</q-item-label>
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
              <btn
                flat
                round
                style="color: #f14a3b"
                icon="mdi-trash-can-outline"
                @click="coachStore.removeUser(props.row.id)"
                glow-color="red-2"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, onMounted} from '@vue/runtime-core'
import {useCoachStore} from "../../stores/useCoachStore"
import {ref} from 'vue'
import {exportFile, useQuasar} from 'quasar'
import SegmentedControl from '../../components/SegmentedControl.vue'
import { User } from '../../models/User'
import AddUser from "./AddUser.vue";
import {useAuthenticationStore} from "../../stores/useAuthenticationStore";
import router from "../../router";

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
    align: 'left' as const,
    field: 'name',
    sortable: true,
  },
  {
    name: 'role',
    required: true,
    label: 'Role',
    align: 'left' as const,
    field: 'role',
    sortable: true,
  },
  {
    name: 'assignedto',
    required: false,
    label: 'Assigned To',
    align: 'left' as const,
    field: 'assignedto',
    sortable: true,
  },
  {
    name: 'email',
    align: 'right' as const,
    label: 'Email',
    field: 'email',
    sortable: true,
  },
  {
    name: 'action',
    align: 'right' as const,
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
  components: {AddUser, SegmentedControl },
  setup() {
    const coachStore = useCoachStore()
    const q = useQuasar()
    
    coachStore.loadUsers();

    return {
      authenticationStore: useAuthenticationStore(),
      newUserDialog: ref(false),
      active: ref(true),
      filter: ref(''),
      roleFilter: ref('all'),
      columns,
      roles,
      coachStore,
      q
    }
  },
  beforeMount() {
    if (!this.authenticationStore.loggedInUser?.isAdmin) {
      router.replace('/projects')
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
//     exportTable() {
//       // naive encoding to csv format
//       const current = new Date()
//       const cDate =
//         current.getFullYear() +
//         '' +
//         (current.getMonth() + 1) +
//         '' +
//         current.getDate()
//       const cTime =
//         current.getHours() + '' + current.getMinutes() + current.getSeconds()
//       const dateTime = cDate + '' + cTime
//       const content = [
//         columns.slice(0, -1).map((col) => wrapCsvValue(col.label)),
//       ]
//         .concat(
//           this.coachStore.users.map((row: { [x: string]: any }) =>
//             columns
//               .slice(0, -1)
//               .map((col) =>
//                 wrapCsvValue(
//                   typeof col.field === 'function'
//                     ? col.field(row)
//                     : row[col.field === void 0 ? col.name : col.field],
//                   col.format
//                 )
//               )
//               .join(',')
//           )
//         )
//         .join('\r\n')
// 
//       const status = exportFile(
//         'table-export-' + dateTime + '.csv',
//         content,
//         'text/csv'
//       )
// 
//       if (status !== true) {
//         this.q.notify({
//           message: 'Browser denied file download...',
//           color: 'negative',
//           icon: 'warning',
//         })
//       }
//     },
    // Not so clean method for updating the role of an user. This is done this way because pinia events don't work in production mode andthe vue watcher doesn't work here.
    updateRole(user: User, oldRole: string) {
      // nextTick is used cause the user param contains the old role. We need to wait for the next tick to get the new role.
      this!.$nextTick(() => {
        this.coachStore
        .updateRole(user)
        .catch((error) => {
            this.q.notify({
            icon: 'warning',
            color: 'warning',
            message: error.detail,
            textColor: 'black'
          });
          this.coachStore.users.find((u: User) => u.id === user.id)!.role = oldRole
        })
      })
      
    }
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
  /* bg color is important for th; just specify one */
  background-color: $yellow-7
</style>
