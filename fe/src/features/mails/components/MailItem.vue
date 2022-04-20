<template>
  <q-item :key="mail.id">
    <q-item-section>
      <q-item-label>By {{ typeof(mail.sender) === 'string' ? mail.sender : mail.sender.fullName }}</q-item-label>
      <q-item-label caption lines="2">{{ mail.info }}</q-item-label>
    </q-item-section>

    <q-item-section side top>
      <q-item-label caption>{{ mail.time }}</q-item-label>
      <btn v-if="!removed"
           tabindex="-1"
           class="gt-xs"
           size="sm"
           flat
           dense
           round
           icon="delete"
           @click="() => {
             removed = true
             prepareRemove(mail)
           }"
      />
      <btn v-else label="undo" @click="stop" dense style="justify-content: center; height: 30px"/>
    </q-item-section>
  </q-item>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useStudentStore} from "../../../stores/useStudentStore";
import {Student} from "../../../models/Student";
import {Mail} from "../../../models/Mail";
import {ref} from "vue";

export default defineComponent({
  props: {
    student: {
      type: Student,
      required: true
    },
    mail: {
      type: Mail,
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
    let timeout: any | null = null

    return {
      show: ref(true),
      removed: ref(false),
      timeout,
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
    },
    stop() {
      this.removed = false
      if (!this.timeout) return
      clearTimeout(this.timeout)
      this.timeout = null
    },
    prepareRemove(mail: Mail) {
      this.timeout = setTimeout(() => {
        this.remove(mail)
        this.timeout = null
      }, 2000)
    },
    remove(mail: Mail) {
      this.show = false
      setTimeout(() => {
        this.deleteMail(mail)
      }, 500)
      return
    },
  }
})
</script>
