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
          Sent Mails
        </div>
        <q-space />
        <q-input
          v-model="studentStore.searchMails"
          outlined
          dense
          debounce="300"
          color="yellow-4"
          placeholder="Search"
          @update:modelValue="studentStore.loadStudentsMails"
        >
          <template #append>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>

      <q-table
        class="my-table mail-table shadow-4"
        :rows="studentStore.mailStudents"
        :columns="columns"
        row-key="id"
        separator="horizontal"
      >
        <template #body="props">
          <q-tr
            :class="props.rowIndex % 2 == 1 ? 'bg-yellow-1' : ''"
            :props="props"
          >
            <q-td auto-width>
              <q-icon
                @click="() => clickRow(props, props.row)"
                size="sm" color="yellow" :name="props.expand ? 'mdi-chevron-up' : 'mdi-chevron-down'" />
            </q-td>
            <q-td
              key="name"
              :props="props"
            >
              {{ props.row.fullName }}
            </q-td>
            <q-td
              key="status"
              :props="props"
            >
              {{status.find(s => s.value === props.row.status).label}}
              
            </q-td>
            <q-td
              key="email"
              :props="props"
            >
              <a :href="'mailto:' + props.row.email" style="color: black">{{ props.row.email }}</a>
            </q-td>
            <q-td style="align-content: flex-end">
              <q-btn
                size="sm" color="yellow" round dense icon="mail" @click="resetDate"
              >
                <q-menu>
                  <q-list>
                    <q-item tag="label">
                      <div class="column q-gutter-sm">
                        <label>Add new mail:</label>
                        <q-input filled v-model="date">
                          <template v-slot:prepend>
                            <q-icon name="event" class="cursor-pointer">
                              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                <q-date v-model="date" mask="YYYY-MM-DD HH:mm">
                                  <div class="row items-center justify-end">
                                    <q-btn v-close-popup label="Close" color="primary" flat />
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
                                    <q-btn v-close-popup label="Close" color="primary" flat />
                                  </div>
                                </q-time>
                              </q-popup-proxy>
                            </q-icon>
                          </template>
                        </q-input>

                        <q-input
                          label="Info"
                          v-model="info"
                          filled
                          type="textarea"
                        />

                        <q-btn class="bg-yellow" @click="() => this.sendMail(props.row)" v-close-popup>
                          Send
                        </q-btn>
                      </div>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </q-td>
          </q-tr>
          <q-tr no-hover v-if="props.expand" :props="props">
            <q-td colspan="100%" :key="emailKey">
              <MailsOverview :student="props.row" />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {ref} from 'vue'
import {Student} from "../../models/Student";
import {useStudentStore} from "../../stores/useStudentStore";
import {useQuasar} from "quasar";
import status from "./Status";
import MailsOverview from "./components/MailsOverview.vue";

const columns = [
  {
    name: 'visibility',
    required: false,
    label: '',
    align: 'left' as const,
    field: '',
    sortable: false,
  },
  {
    name: 'name',
    required: true,
    label: 'Name',
    align: 'left' as const,
    field: 'name',
    sortable: true,
  },
  {
    name: 'status',
    required: true,
    label: 'Status',
    align: 'left' as const,
    field: 'status',
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
    name: 'sendEmail',
    align: 'left' as const,
    label: '',
    field: '',
    sortable: false,
  },
]

export default defineComponent({
  components: {MailsOverview},
  setup() {
    const studentStore = useStudentStore()
    const q = useQuasar()

    const today = new Date();
    const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    const dateTime = date + ' ' + time;

    return {
      studentStore,
      filter: ref(''),
      info: ref(''),
      date: ref(dateTime),
      columns,
      status,
      q
    }
  },
  data() {
    return {
      emailKey: 0
    }
  },
  created() {
    this.studentStore.loadStudentsMails()
  },
  methods: {
    updateStatus(student: Student, oldStatus: string) {
      this!.$nextTick(() => {
        this.studentStore
          .updateStatus(student)
          .catch((error) => {
            this.q.notify({
              icon: 'warning',
              color: 'warning',
              message: error.detail,
              textColor: 'black'
            });
            this.studentStore.students.find((s: Student) => s.id === student.id)!.status = oldStatus
          })
      })
    },
    clickRow(props: any, student: Student) {
      props.expand = !props.expand
      if (props.expand) this.studentStore.getMails(student)
    },
    resetDate() {
      const today = new Date();
      const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
      const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      this.date = date + ' ' + time
    },
    async sendMail(student: Student) {
      await this.studentStore.sendMail(student, this.date, this.info)
      await this.studentStore.getMails(student)

      this.info = ''

      this.emailKey += 1
    }
  }
})
</script>

<style scoped>
.mail-table {
  border-radius: 10px;
}
</style>
