<template>
  <q-stepper
    flat
    v-model="currentStep"
    header-nav
    ref="stepper"
    active-color="yellow"
    active-icon="none"
    class="text-weight-medium"
    animated
  >
    <q-step
      v-for="step in steps"
      :key="step.state"
      :name="step.state"
      :title="step.name"
      :icon="step.icon"
      :done="currentstepids.includes(step.state)"
      >
      <q-input
        v-if="!currentsteps.find(s => parseInt(s.info) === step.state)"
        outlined 
        style="width: fit-content" 
        v-model="date"
        :disable="currentstepids.includes(step.state)"
        >
        <template v-slot:prepend>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy cover transition-show="scale" transition-hide="scale">
              <q-date 
                v-model="date"
                mask="YYYY-MM-DD HH:mm"
                >
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
      <div v-else>
        <!-- <div> -->
        Sent at {{currentsteps.find(s => parseInt(s.info) === step.state).time}}
        <!-- </div> -->
        
      </div>
      <!-- <q-input
        label="Email"
        v-model="step.email"
        outlined
        type="textarea"
        color="yellow"
      /> -->
      
      <q-stepper-navigation>
        <btn
          :disable="currentstepids.includes(step.state)"
          color="yellow"
          @click="() => { this.info=step.state; sendMail(), currentStep++; }"
          label="Mark as sent"
          shadow-color="orange"
          shadow-strength="2"
        />
        <btn
          v-if="currentsteps.find(s => parseInt(s.info) === step.state)"
          label="Delete"
          color="red"
          class="q-mx-md"
          shadow-color="red"
          shadow-strength="2"
          @click="() => { deleteMail(currentsteps.find(m => parseInt(m.info) === step.state))}"
        />
      </q-stepper-navigation>
    </q-step>
  </q-stepper>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useStudentStore} from "../../../stores/useStudentStore";
import {Student} from "../../../models/Student";
import {Mail} from "../../../models/Mail";
import {ref} from "vue";

enum ApprovalStates {
  Applied = 1,
  Awaiting = 2,
  Approved = 3,
  ContractConfirmed = 4,
  ContractDeclined = 5,
  Rejected = 6
}

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
    let timeout: any | null = null
    const today = new Date();
    const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    const dateTime = date + ' ' + time;
    const statuses = [ApprovalStates.Applied, ApprovalStates.Awaiting, ApprovalStates.Approved, ApprovalStates.ContractConfirmed, ApprovalStates.ContractDeclined, ApprovalStates.Rejected]
    return {
      emailKey: 0,
      show: ref(true),
      removed: ref(false),
      date: ref(dateTime),
      timeout,
      statuses,
      currentStep: ref(null),
      steps: [
        {
          state: ApprovalStates.Applied,
          icon: 'grade',
          name: 'Applied'
        },
        {
          state: ApprovalStates.Awaiting,
          name: 'Awaiting',
          icon: 'schedule',
        },
        {
          state: ApprovalStates.Approved,
          name: 'Approved/Rejected',
          icon: 'check',
        },
        {
          state: ApprovalStates.ContractConfirmed,
          name: 'Contract Confirmed/Declined',
          icon: 'playlist_add_check',
        },
      ],
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
    async sendMail() {
      await this.studentStore.sendMail(this.student, this.date, this.info)
      await this.studentStore.getMails(this.student)
    
      this.info = ''
      this.resetDate()
      this.emailKey += 1
    },
    stop() {
      this.removed = false
      if (!this.timeout) return
      clearTimeout(this.timeout)
      this.timeout = null
    },
    prepareRemove(mail: Mail) {
      console.log(mail)
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
    
    resetDate() {
      const today = new Date();
      const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
      const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      this.date = date + ' ' + time
    },
  },
  computed: {
    currentsteps() {
      const mails = this.studentStore.mails
      console.log(mails)
      if (!this.studentStore.mails.has(this.student.id)) return []
      const data = (this.studentStore.mails.get(this.student.id) ?? []).filter(mail => {
        return this.statuses.includes(parseInt(mail.info))
      })
      if (!this.currentStep) {
        this.currentStep = this.statuses.find(s => !data.map(d=>parseInt(d.info)).includes(s))
      }
      return data
    },
    currentstepids() {
      return this.currentsteps.map(s => parseInt(s.info))
    },
  }
})
</script>


