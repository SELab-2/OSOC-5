<template>
  <div
    class="relative-position flex justify-center"
  >
    <div
      class="q-pa-md q-gutter-md"
    >
      <div class="text-bold text-h4">
        Sent Mails
      </div>
      <div class="row">
        <div class="row col-6 q-gutter-sm">
          <q-input
            v-model="search"
            outlined
            dense
            debounce="300"
            color="yellow-4"
            placeholder="Search"
            @update:modelValue="async () => await mailStore.loadStudentsMails(filters, (count: number) => pagination.rowsNumber = count)"
          >
            <template #append>
              <q-icon name="search" />
            </template>
          </q-input>
          <q-select
            v-model="statusFilter"
            class="col"
            rounded
            outlined
            dense
            multiple
            clearable
            use-chips
            color="yellow"
            label="Status"
            :options="status"
            map-options
            emit-value
            @update:model-value="async () => await mailStore.loadStudentsMails(filters, (count: number) => pagination.rowsNumber = count)"
          />
        </div>
        <div class="row no-wrap col-6 q-gutter-sm justify-end">
          <q-select
            v-model="statusUpdate"
            style="width: 220px"
            rounded
            outlined
            color="yellow"
            dense
            use-chips
            emit-value
            map-options
            label="New status"
            :options="status"
          />
          <q-button>
            <btn
              padding="7px"
              color="yellow"
              shadow-color="orange"
              shadow-strength=2
              no-wrap
              @click="updateStatusStudents"
            >
              Bulk update status
            </btn>
          </q-button>
        </div>
      </div>
      <q-table
        v-model:selected="selectedStudents"
        class="cornered shadow-4"
        :rows="mailStore.mailStudents"
        :columns="mailsColumns"
        :loading="mailStore.isLoading"
        :pagination="pagination"
        :rows-per-page-options="[ 3, 5, 7, 10, 15, 20, 25, 50 ]"
        row-key="url"
        selection="multiple"
        separator="horizontal"
        @request="onRequest"
        :table-class="$q.dark.isActive ? 'bg-dark2' : ''"
        :table-header-class="`${$q.dark.isActive ? 'text-black' : ''} bg-yellow`"
      >
        <template #body="props">
          <q-tr
            :class="props.rowIndex % 2 == 1 && !$q.dark.isActive ? 'bg-yellow-1' : ''"
            :style="`background-color: ${props.rowIndex % 2 == 1 && $q.dark.isActive ? colors.lighten(colors.getPaletteColor('yellow'),-75) : ''}`"
          >
            <q-td>
              <q-checkbox color="yellow" v-model="props.selected" />
            </q-td>
            <q-td auto-width>
              <q-icon
                size="sm"
                color="yellow"
                :name="props.expand ? 'mdi-chevron-up' : 'mdi-chevron-down'"
                @click="() => clickRow(props, props.row)"
              />
            </q-td>
            <q-td
              key="name"
              :props="props"
              style="max-width: 20vw; overflow: hidden;  white-space: nowrap; text-overflow: ellipsis;"
              :title="props.row.fullName"
            >
              {{ props.row.fullName }}
            </q-td>
            <q-td
              key="status"
              :props="props"
            >
              <q-select
                v-model="props.row.status"
                v-ripple
                color="yellow"
                borderless
                dense
                style="border-radius: 5px; position: relative; width: 170px"
                :options="status"
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
                    @click="() => updateStatus(props.row, props.row.status)"
                  >
                    <q-item-section>
                      <q-item-label>{{ scope.opt.label }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
            </q-td>
            <q-td
              key="email"
              :props="props"
              style="max-width: 20vw; overflow: hidden;  white-space: nowrap; text-overflow: ellipsis;"
              :title="props.row.email"
            >
              <a
                :href="'mailto:' + props.row.email"
                :class="`text-${$q.dark.isActive ? 'white' : 'black'}`"
              >{{ props.row.email }}</a>
            </q-td>
            <q-td style="align-content: flex-end">
              <btn
                dense color="yellow" glow-size="250px" flat icon="forward_to_inbox" @click="reset"
              >
                <q-menu>
                  <q-list>
                    <q-item tag="label">
                      <div class="column q-gutter-sm">
                        <label>Add new mail:</label>
                        <q-input outlined color="yellow" v-model="date">
                          <template v-slot:prepend>
                            <q-icon name="event" class="cursor-pointer">
                              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                <q-date v-model="date" mask="YYYY-MM-DD HH:mm">
                                  <div class="row items-center justify-end">
                                    <q-btn v-close-popup label="Close" color="yellow" flat />
                                  </div>
                                </q-date>
                              </q-popup-proxy>
                            </q-icon>
                          </template>

                          <template v-slot:append>
                            <q-icon name="access_time" class="cursor-pointer">
                              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                <q-time v-model="date" mask="YYYY-MM-DD HH:mm" format24h>
                                  <div class="row items-center justify-end">
                                    <q-btn v-close-popup label="Close" color="yellow" flat />
                                  </div>
                                </q-time>
                              </q-popup-proxy>
                            </q-icon>
                          </template>
                        </q-input>

                        <q-input
                          label="Info"
                          v-model="info"
                          outlined
                          color="yellow"
                          type="textarea"
                        />

                        <btn color="yellow" shadow-color="orange" @click="() => sendMail(props.row)" v-close-popup>
                          Send
                        </btn>
                      </div>
                    </q-item>
                  </q-list>
                </q-menu>
              </btn>
            </q-td>
          </q-tr>
          <q-tr
            v-if="props.expand"
            no-hover
            :props="props"
          >
            <q-td colspan="100%">
              <MailsOverview
                :student="props.row"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {Ref, ref} from 'vue'
import {Student} from "../../models/Student";
import {useQuasar, colors} from "quasar";
import status from "./Status";
import MailsOverview from "./components/MailsOverview.vue";
import {useMailStore} from "../../stores/useMailStore";
import columnsMails from "../../models/MailStudentColumns";
import router from "../../router";
import {useAuthenticationStore} from "../../stores/useAuthenticationStore";
import mailsColumns from "../../models/MailsColumns";

export default defineComponent({
  components: {MailsOverview},
  setup() {
    const mailStore = useMailStore()
    const q = useQuasar()

    return {
      mailStore,
      authenticationStore: useAuthenticationStore(),
      filter: ref(''),
      statusUpdate: ref(null),
      selectedStudents: ref([]),
      mailsColumns,
      columnsMails,
      status,
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
      search: ref(''),
      statusFilter: ref([]),
      date: ref((new Date()).toLocaleString()),
      info: ref(''),
      pagination
    }
  },
  beforeMount() {
    if (!this.authenticationStore.loggedInUser?.isAdmin) {
      router.replace('/notfound')
    }
  },
  async mounted() {
    await this.mailStore.loadStudentsMails(this.filters, (count: number) => this.pagination.rowsNumber = count)
  },
  computed: {
    filters() {
      let filter = {} as {
        search: string
        page_size: number
        page: number
        ordering: string
        status: string
      }

      if (this.search) filter.search = this.search
      filter.page_size = this.pagination.rowsPerPage
      filter.page = this.pagination.page
      const order = this.pagination.descending ? '-' : ''
      if (this.pagination.sortBy === 'name') {
          filter.ordering = `${order}first_name,${order}last_name`
      } else if (this.pagination.sortBy !== null) {
          filter.ordering = `${order}${this.pagination.sortBy}`
      }
      if (this.statusFilter && this.statusFilter.length > 0) filter.status = this.statusFilter.join(',')

      return filter
    }
  },
  methods: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    reset() {
      this.date = (new Date()).toLocaleString()
      this.info = ''
    },
    async sendMail(student: Student) {
      await this.mailStore.sendMail(student, null, this.date, this.info)
      await this.mailStore.getMails(student)
    },
    async onRequest(props: any) {
      this.pagination = props.pagination
      await this.mailStore.loadStudentsMails(this.filters, (count: number) => this.pagination.rowsNumber = count)
    },
    async updateStatusStudents() {
      if (this.statusUpdate !== null) {
        await this.mailStore.updateStatusStudents(this.statusUpdate, this.selectedStudents)
        this.selectedStudents = []
        this.statusUpdate = null
        await this.mailStore.loadStudentsMails(this.pagination, (count: number) => this.pagination.rowsNumber = count)
      }
    },
    updateStatus(student: Student, oldStatus: number) {
      this?.$nextTick(() => {
        this.mailStore
          .updateStatus(student)
          .catch((error) => {
            this.q.notify({
              icon: 'warning',
              color: 'warning',
              message: error.detail,
              textColor: 'black'
            });
            const student = this.mailStore.mailStudents.find((s: Student) => s.id === student.id) as Student
            if(student)
              student.status = oldStatus
          })
      })
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    clickRow(props: any, student: Student) {
      props.expand = !props.expand
      if (props.expand) this.mailStore.getMails(student)
    },
  }
})
</script>