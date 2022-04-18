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
            @click="props.expand = !props.expand"
            :class="props.rowIndex % 2 == 1 ? 'bg-yellow-1' : ''"
            :props="props"
          >
            <q-td auto-width>
              <q-icon size="sm" color="yellow" :name="props.expand ? 'mdi-chevron-up' : 'mdi-chevron-down'" />
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
              {{ props.row.email }}
            </q-td>
          </q-tr>
          <q-tr v-show="props.expand" :props="props">
            <q-td colspan="100%">
              <div class="text-left">This is expand slot for row above: {{ props.row.fullName }}.</div>
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
import { Student } from "../../models/Student";
import { useStudentStore } from "../../stores/useStudentStore";
import {useQuasar} from "quasar";
import status from "./Status";

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
]

export default defineComponent({
  setup() {
    const studentStore = useStudentStore()
    const q = useQuasar()

    return {
      studentStore,
      filter: ref(''),
      columns,
      status,
      q
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
    }
  }
})
</script>

<style scoped>
.mail-table {
  border-radius: 10px;
}
</style>