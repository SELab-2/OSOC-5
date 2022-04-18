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

      <q-table
        class="my-table mail-table shadow-4"
        :rows="studentStore.students"
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
              <q-btn size="sm" color="yellow" round dense @click="props.expand = !props.expand" :icon="props.expand ? 'remove' : 'add'" />
            </q-td>
            <q-td
              key="name"
              :props="props"
            >
              {{ props.row.fullName }}
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
import { useStudentStore } from "../../stores/useStudentStore";

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

    return {
      studentStore,
      filter: ref(''),
      columns
    }
  },
  created() {
    this.studentStore.loadStudents()
  }
})
</script>

<style scoped>
.mail-table {
  border-radius: 10px;
}
</style>