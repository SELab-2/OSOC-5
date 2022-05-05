<template>
  <q-stepper
    ref="stepper"
    v-model="currentStep"
    flat
    header-nav
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
        v-model="date" 
        outlined 
        style="width: fit-content"
        :disable="currentstepids.includes(step.state)"
      >
        <template #prepend>
          <q-icon
            name="event"
            class="cursor-pointer"
          >
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
              <q-date 
                v-model="date"
                mask="YYYY-MM-DD HH:mm"
              >
                <div class="row items-center justify-end">
                  <q-btn
                    v-close-popup
                    label="Close"
                    color="primary"
                    flat
                  />
                </div>
              </q-date>
            </q-popup-proxy>
          </q-icon>
        </template>
      
        <template #append>
          <q-icon
            name="access_time"
            class="cursor-pointer"
          >
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
              <q-time
                v-model="date"
                mask="YYYY-MM-DD HH:mm"
                format24h
              >
                <div class="row items-center justify-end">
                  <q-btn
                    v-close-popup
                    label="Close"
                    color="primary"
                    flat
                  />
                </div>
              </q-time>
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
      <div v-else>
        <!-- <div> -->
        Sent at {{ currentsteps.find(s => parseInt(s.info) === step.state)?.time ?? 'unknown time' }}
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
          label="Mark as sent"
          shadow-color="orange"
          shadow-strength="2"
          @click="onclickmail(step.state)"
        />
        <btn
          v-if="currentsteps.find(s => parseInt(s.info) === step.state)"
          label="Delete"
          color="red"
          class="q-mx-md"
          shadow-color="red"
          shadow-strength="2"
          @click="() => { deleteMail(currentsteps.find(m => parseInt(m.info) === step.state)!)}"
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
import {ref, Ref} from "vue";
import {useMailStore} from "../../../stores/useMailStore";

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
    const mailStore = useMailStore()

    return {
      mailStore,
    }
  },
  data() {
    let timeout: any | null = null
    const today = new Date();
    const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    const dateTime = date + ' ' + time;
    const statuses = [ApprovalStates.Applied, ApprovalStates.Awaiting, ApprovalStates.Approved, ApprovalStates.ContractConfirmed, ApprovalStates.ContractDeclined, ApprovalStates.Rejected]
    const currentStep: Ref<ApprovalStates | undefined> = ref(undefined)
    return {
      emailKey: 0,
      show: ref(true),
      removed: ref(false),
      date: ref(dateTime),
      timeout,
      statuses,
      info: '',
      currentStep,
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
  computed: {
    currentsteps() {
      const mails = this.mailStore.mails
      if (!this.mailStore.mails.has(this.student.id)) return []
      const data = (this.mailStore.mails.get(this.student.id) ?? []).filter(mail => {
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
  },
  mounted() {
    this.mailStore.getMails(this.student)
  },
  methods: {
    async deleteMail(mail: Mail) {
      await this.mailStore.deleteMail(mail)
      await this.mailStore.getMails(this.student)

      this.emailKey += 1
    },
    onclickmail(status: number) {
      this.info = status.toString();
      this.sendMail();
      if (this.currentStep) this.currentStep++;
    },
    async sendMail() {
      await this.mailStore.sendMail(this.student, this.date, this.info)
      await this.mailStore.getMails(this.student)

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
  }
})
</script>


