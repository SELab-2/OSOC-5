<template>
  <div
    class="relative-position flex justify-center"
  >
    <div
      class="q-pa-md q-gutter-md"
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
          <btn
            color="yellow"
            icon-right="add"
            class="text-black"
            label="Add User"
            shadow-color="orange"
            shadow-strength="2"
            @click="newUserDialog = true"
          />
        </div>
        <div class="row q-px-sm">
          <q-space />
          <q-dialog v-model="newUserDialog">
            <q-card>
              <AddUser :created="async () => await coachStore.loadUsersCoaches(filters, (count: number) => pagination.rowsNumber = count)" />
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
        v-model:pagination="pagination"
        class="cornered shadow-4"
        :rows="coachStore.users"
        :columns="userColumns"
        :rows-per-page-options="[ 3, 5, 7, 10, 15, 20, 25, 50 ]"
        row-key="id"
        separator="horizontal"
        :loading="coachStore.isLoading"
        @request="onRequest"
        :table-class="$q.dark.isActive ? 'bg-dark2' : ''"
        :table-header-class="`${$q.dark.isActive ? 'text-black' : ''} bg-yellow`"
      >
        <template #body="props">
          <q-tr
            :class="props.rowIndex % 2 == 1 && !$q.dark.isActive ? 'bg-yellow-1' : ''"
            :style="`background-color: ${props.rowIndex % 2 == 1 && $q.dark.isActive ? colors.lighten(colors.getPaletteColor('yellow'),-75) : ''}`"
          >
            <q-td
              key="name"
              style="max-width: 20vw; overflow: hidden;  white-space: nowrap; text-overflow: ellipsis;"
              :title="props.row.fullName"
            >
              {{ props.row.fullName }}
            </q-td>
            <q-td
              key="role"
            >
              <q-select
                v-model="props.row.role"
                v-ripple
                v-if="authenticationStore.loggedInUser?.email != props.row.email"
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
                    @click="() => updateRole(props.row, props.row.role)"
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
              <div v-else>{{ roles.find(r => r.value === props.row.role)!.label }}</div>
            </q-td>
            <q-td
              key="assignedto"
              style="max-width: 20vw; overflow: hidden; white-space: nowrap; text-overflow: ellipsis"
              :title="props.row.projects?.map((p: {name: string}) => p.name).join(', ') ?? ''"
            >
              {{ props.row.projects?.map((p: {name: string}) => p.name).join(', ') ?? '' }}
            </q-td>
            <q-td
              key="email"
              style="max-width: 20vw; overflow: hidden;  white-space: nowrap; text-overflow: ellipsis;"
              :title="props.row.email"
            >
              {{ props.row.email }}
            </q-td>
            <q-td
              key="remove"
            >
              <btn
                v-if="authenticationStore.loggedInUser?.email !== props.row.email"
                flat
                round
                style="color: #f14a3b"
                icon="mdi-trash-can-outline"
                glow-color="red-2"
                @click="() => deleteUserMethod(props.row)"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>

      <q-dialog
        :model-value="userId !== -1"
        @update:model-value="userId = -1"
      >
        <DeleteDialog
          :name="userName"
          type="user"
          :delete="() => removeUser(userId)"
        />
      </q-dialog>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from '@vue/runtime-core'
import {useCoachStore} from "../../stores/useCoachStore"
import {ref} from 'vue'
import {exportFile, useQuasar, colors} from 'quasar'
import SegmentedControl from '../../components/SegmentedControl.vue'
import DeleteDialog from "../../components/DeleteDialog.vue";
import { User } from '../../models/User'
import AddUser from "./AddUser.vue";
import userColumns from "../../models/UserColumns";
import {useAuthenticationStore} from "../../stores/useAuthenticationStore";
import router from "../../router";
import roles from "../../models/UserRoles";

export default defineComponent({
  components: {AddUser, SegmentedControl, DeleteDialog },
  name: 'Users',
  setup() {
    const coachStore = useCoachStore()
    const q = useQuasar()

    return {
      authenticationStore: useAuthenticationStore(),
      newUserDialog: ref(false),
      active: ref(true),
      filter: ref(''),
      roleFilter: ref('all'),
      userColumns,
      roles,
      coachStore,
      q,
      colors
    }
  },
  data() {
    const pagination = ref({
      sortBy: 'name',
      descending: false,
      page: 1,
      rowsPerPage: 10,
      rowsNumber: 10 // if getting data from a server
    })

    return {
      pagination,
      deleteDialog: ref(false),
      userId: ref(-1),
      userName: ref('')
    }
  },
  computed: {
    filters() {
      const filter = {} as {
        search: string
        is_active: boolean
        is_admin: boolean
        ordering: string
        page: number
        page_size: number
      }

      if (this.filter) filter.search = this.filter
      filter.page_size = this.pagination.rowsPerPage
      filter.page = this.pagination.page
      if (this.roleFilter === 'inactive') filter.is_active = false
      if (this.roleFilter === 'admin') {
        filter.is_active = true
        filter.is_admin = true
      }
      if (this.roleFilter === 'coach'){
        filter.is_active = true
        filter.is_admin = false
      }
      const order = this.pagination.descending ? '-' : ''
      if (this.pagination.sortBy === 'name') {
        filter.ordering = `${order}first_name,${order}last_name`
      } else if (this.pagination.sortBy === 'role') {
        const order = this.pagination.descending ? '' : '-'
        filter.ordering = `${order}is_admin,${order}is_active`
      } else if (this.pagination.sortBy !== null) {
        filter.ordering = `${order}${this.pagination.sortBy}`
      }

      return filter
    }
  },
  beforeMount() {
    if (!this.authenticationStore.loggedInUser?.isAdmin) {
      router.replace('/notfound')
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
    deleteUserMethod(props: any) {
      this.userId = props.id
      this.userName = props.fullName
    },
    async removeUser(id: number) {
      await this.coachStore.removeUser(id, () => {
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Successfully deleted!',
          })
        },
        () => this.$q.notify({
          icon: "close",
          color: "negative",
          message: "Failed to delete!"
        }))

      if (this.coachStore.users.length === 1 && this.pagination.page != 0) {
        this.pagination.page -= 1
      }
      this.pagination.rowsNumber -= 1

      this.coachStore.loadUsersCoaches(this.filters, (count: number) => this.pagination.rowsNumber = count)
    },
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
  watch: {
    filters() {
      this.coachStore.loadUsersCoaches(this.filters, (count: number) => this.pagination.rowsNumber = count);
    }
  },
  activated() {
    if (this.coachStore.shouldRefresh) {
      this.coachStore.loadUsersCoaches(this.filters, (count: number) => this.pagination.rowsNumber = count);
    }
  }
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
</style>
