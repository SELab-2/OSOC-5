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
    </div>

    <q-table
      class="my-table mail-table shadow-4"
      :rows="studentStore.students"
      :columns="columns"
      row-key="id"
      separator="horizontal"
    >
    </q-table>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {ref} from 'vue'
import { Student } from "../../models/Student";
import { useStudentStore } from "../../stores/useStudentStore";

const columns = [
  {
    name: 'name',
    required: true,
    label: 'Name',
    align: 'left' as const,
    field: (row: Student) => row.firstName + ' ' + row.lastName,
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