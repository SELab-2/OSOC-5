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
          v-model="mailStore.searchMails"
          outlined
          dense
          debounce="300"
          color="yellow-4"
          placeholder="Search"
          @update:modelValue="mailStore.loadStudentsMails"
        >
          <template #append>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>
      <div class="q-pl-md full-width">
        <q-select
          v-model="statusFilter"
          rounded
          outlined
          dense
          multiple
          clearable
          use-chips
          label="Status"
          :options="status"
        />
      </div>
      <q-table
        v-model:selected="mailStore.selectedStudents"
        class="my-table mail-table shadow-4"
        :rows="mailStore.mailStudents"
        :columns="mailsColumns"
        :loading="mailStore.isLoading"
        row-key="url"
        selection="multiple"
        separator="horizontal"
      >
        <template #body="props">
          <q-tr
            :class="props.rowIndex % 2 == 1 ? 'bg-yellow-1' : ''"
            :props="props"
          >
            <q-td>
              <q-checkbox v-model="props.selected" />
            </q-td>
            <q-td auto-width>
              <q-icon
                @click="() => clickRow(props, props.row)"
                size="sm" color="yellow" :name="props.expand ? 'mdi-chevron-up' : 'mdi-chevron-down'"
              />
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
                    @click="() => updateStatus(props.row, props.row.status)"
                    class="items-center"
                    v-bind="scope.itemProps"
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
            >
              <a :href="'mailto:' + props.row.email" style="color: black">{{ props.row.email }}</a>
            </q-td>

          </q-tr>
          <q-tr no-hover v-if="props.expand" :props="props">
            <q-td colspan="100%">
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
import {useQuasar} from "quasar";
import status from "./Status";
import MailsOverview from "./components/MailsOverview.vue";
import {useMailStore} from "../../stores/useMailStore";
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
      statusFilter: ref([]),
      mailsColumns,
      status,
      q
    }
  },
  beforeMount() {
    if (!this.authenticationStore.loggedInUser?.isAdmin) {
      router.replace('/projects')
    }
  },
  mounted() {
    this.mailStore.loadStudentsMails()
  },
  methods: {
    updateStatus(student: Student, oldStatus: string) {
      this!.$nextTick(() => {
        this.mailStore
          .updateStatus(student)
          .catch((error) => {
            this.q.notify({
              icon: 'warning',
              color: 'warning',
              message: error.detail,
              textColor: 'black'
            });
            this.mailStore.mailStudents.find((s: Student) => s.id === student.id)!.status = oldStatus
          })
      })
    },
    clickRow(props: any, student: Student) {
      props.expand = !props.expand
      if (props.expand) this.mailStore.getMails(student)
    },
  }
})
</script>

<style scoped>
.mail-table {
  border-radius: 10px;
}
</style>
