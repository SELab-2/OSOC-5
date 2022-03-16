<template>
  <div class="q-pa-md q-gutter-md">
    <div class="row">
      <div class="col-9">
        <h class="text-bold text-h4"> Users</h>
      </div>
      <div class="col-3">
        <q-btn
          stack
          flat
          color="secondary"
          icon="download"
          label="csv"
          @click="exportTable"
        />
      </div>
    </div>
    <div class="row q-mb-md vertical-middle">
      <SegmentedControl v-model="roleFilter" 
        :options="[
          { name: 'all', label: 'All' }, 
          { name:'admin', label: 'Admins' },
          { name: 'coach', label: 'Coaches' },
          { name: 'disabled', label: 'Disabled' }
        ]"
        />
        
        <q-space />
        <q-input outlined dense debounce="300" v-model="filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
    </div>
    <q-table
      class="my-table user-table shadow-4"
      :rows="users"
      :columns="columns"
      row-key="id"
      :pagination="pagination"
      separator="horizontal"
    >
      <template v-slot:body="props">
        <q-tr
          :class="props.rowIndex % 2 == 1 ? 'bg-yellow-1' : ''"
          :props="props"
        >
          <q-td key="name" @click="console.log(props)" :props="props">
            {{ props.row.name }}
          </q-td>
          <q-td key="role" :props="props">
            <q-select
              v-ripple
              borderless
              dense
              style="border-radius: 5px; position: relative; width: 80px"
              v-model="props.row.role"
              :options="roles"
              transition-show="jump-down"
              transition-hide="jump-up"
              transition-duration="300"
              behavior="menu"
              map-options
              emit-value
            >
              <template v-slot:option="scope">
                <q-item class="items-center" v-bind="scope.itemProps">
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
          <q-td key="assignedto" :props="props"
            >{{ props.row.assignedto }}
          </q-td>
          <q-td key="email" :props="props">{{ props.row.email }} </q-td>
          <q-td style="width: 10px" key="remove">
            <q-btn
              flat
              round
              style="color: #f14a3b"
              icon="mdi-trash-can-outline"
            />
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { exportFile } from 'quasar'
import SegmentedControl from './SegmentedControl.vue'

function wrapCsvValue (val, formatFn) {
  let formatted = formatFn !== void 0
    ? formatFn(val)
    : val

  formatted = formatted === void 0 || formatted === null
    ? ''
    : String(formatted)

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
    color: 'blue',
  },
  {
    label: 'Coach',
    value: 'coach',
    icon: 'mdi-whistle-outline',
    color: 'green',
  },
  {
    label: 'Disabled',
    value: 'disabled',
    icon: 'mdi-close',
    color: 'red',
  },
]
export default {
  data() {
    return {
      users: [
        {
          id: 123,
          name: 'Miet Claeys',
          email: 'miet@osoc.be',
          role: ref('admin'),
        },
        {
          id: 1234,
          name: 'Wouter Hennen',
          email: 'wouter.hennen@ugent.be',
          role: ref('admin'),
        },
        {
          id: 1235,
          name: 'Lisa De Jonghe',
          email: 'lisa.dejonghe@ugent.be',
          role: ref('admin'),
        },
        {
          id: 1236,
          name: 'Lander Saerens',
          email: 'lander.saerens@ugent.be',
          role: ref('coach'),
          assignedto: 'Project #1',
        },
        {
          id: 1237,
          name: 'Friedrich Vandenberghe',
          email: 'friedrich.vandenberghe@ugent.be',
          role: ref('coach'),
          assignedto: 'Project #2',
        },
        {
          id: 1238,
          name: 'Miet Claeys',
          email: 'miet@osoc.be',
          role: ref('coach'),
          assignedto: 'Project #3',
        },
        {
          id: 1239,
          name: 'Wouter Hennen',
          email: 'wouter.hennen@ugent.be',
          role: ref('coach'),
          assignedto: 'Project #1',
        },
        {
          id: 1230,
          name: 'Lisa De Jonghe',
          email: 'lisa.dejonghe@ugent.be',
          role: ref('disabled'),
        },
        {
          id: 1231,
          name: 'Lander Saerens',
          email: 'lander.saerens@ugent.be',
          role: ref('disabled'),
        },
        {
          id: 1232,
          name: 'Friedrich Vandenberghe',
          email: 'friedrich.vandenberghe@ugent.be',
          role: ref('disabled'),
        },
      ],
    }
  },
  methods: {
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
          this.users.map((row) =>
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
        $q.notify({
          message: 'Browser denied file download...',
          color: 'negative',
          icon: 'warning',
        })
      }
    },
  },
  setup() {
    return {
      active: ref(true),
      columns,
      roles,
    }
  },
}
</script>

<style scoped>
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

<style scoped lang="sass">
.my-table
    thead
        /* bg color is important for th; just specify one */
        background-color: rgba(#FCB70F, .7)
</style>
