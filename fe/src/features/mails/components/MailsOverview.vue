<template>
  <q-list :key="emailKey">
    <q-item v-for="mail in studentStore.mails.get(student.id)" :key="mail.id">
      <q-item-section>
        <q-item-label>By {{ typeof(mail.sender) === 'string' ? mail.sender : mail.sender.fullName }}</q-item-label>
        <q-item-label caption lines="2">{{ mail.info }}</q-item-label>
      </q-item-section>

      <q-item-section side top>
        <q-item-label caption>{{ mail.time }}</q-item-label>
        <q-icon name="delete" color="yellow" @click="() => deleteMail(mail)" />
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useStudentStore} from "../../../stores/useStudentStore";
import {Student} from "../../../models/Student";
import {Mail} from "../../../models/Mail";

export default defineComponent({
  props: {
    student: {
      type: Student,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore,
    }
  },
  data() {
    return {
      emailKey: 0
    }
  },
  created() {
    this.studentStore.getMails(this.student)
  },
  methods: {
    async deleteMail(mail: Mail) {
      await this.studentStore.deleteMail(mail)
      await this.studentStore.getMails(this.student)

      this.emailKey += 1
    }
  }
})
</script>
