<template>
  <div class="row">
    <div class="col-6">
      <q-stepper
        ref="stepper"
        v-model="currentStep"
        flat
        vertical
        header-nav
        active-color="yellow"
        active-icon="none"
        class="text-weight-medium"
        animated
        @before-transition="adaptState"
      >
        <q-step
          v-for="step in steps"
          :key="step.state"
          :name="step.state"
          :title="step.name"
          :icon="step.icon"
          :done="currentstepids.includes(step.state)"
        >
          <div
            v-if="!currentsteps.find(s => parseInt(s.info) === step.state)"
            class="q-gutter-sm"
          >
            <q-input
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
            <q-input
              v-model="info"
              label="Info"
              filled
              type="textarea"
            />

            <div v-if="step.states.length > 1">
              <q-option-group
                :options="step.states"
                type="radio"
                v-model="selected"
              />
            </div>
          </div>
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
              @click="onclickmail()"
            />

            <btn
              v-if="currentsteps.find(s => parseInt(s.info) === step.state)"
              label="Delete"
              color="red"
              class="q-mx-md"
              shadow-color="red"
              shadow-strength="2"
              @click="() => { deleteMail(currentsteps.find(m => parseInt(m.info) === step.state)) }"
            />
          </q-stepper-navigation>
        </q-step>
      </q-stepper>
    </div>
    <div class="col-6 q-pt-lg">
      <q-list>
        <q-item v-for="mail in this.mailStore.mails.get(student.id)" :key="mail.id">
          <q-item-section :avatar="mail.type !== null">
            <q-icon :name="approvalStates.filter(state => state.value === mail.type)[0]?.icon ?? ''" />
          </q-item-section>

          <q-item-section>
            <q-item-label >By {{mail.sender.firstName}} {{mail.sender.lastName}}</q-item-label>
            <q-item-label v-if="mail.info" caption lines="2">{{mail.info}}</q-item-label>
          </q-item-section>

          <q-item-section side top>
            <q-item-label caption>{{ mail.time }}</q-item-label>
            <q-icon name="mdi-trash-can-outline" color="red" @click="deleteMail(mail)" />
          </q-item-section>

          <q-separator spaced inset />
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {Student} from "../../../models/Student";
import {Mail} from "../../../models/Mail";
import {ref, Ref} from "vue";
import {useMailStore} from "../../../stores/useMailStore";
import approvalStates from "../../../models/ApprovalStates";

enum ApprovalStates {
  Applied = 0,
  Awaiting = 1,
  Approved = 2,
  ContractConfirmed = 3,
  ContractDeclined = 4,
  Rejected = 5
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
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let timeout: any | null = null
    const today = new Date();
    const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    const dateTime = date + ' ' + time;
    const statuses = approvalStates.map(state => state.value)

    const steps = [
      {
        state: ApprovalStates.Applied,
        icon: 'grade',
        name: 'Applied',
        states: approvalStates.filter(state => state.value === 0)
      },
      {
        state: ApprovalStates.Awaiting,
        name: 'Awaiting',
        icon: 'schedule',
        states: approvalStates.filter(state => state.value === 1)
      },
      {
        state: ApprovalStates.Approved,
        name: 'Approved/Rejected',
        icon: 'check',
        states: approvalStates.filter(state => state.value === 2 || state.value === 5)
      },
      {
        state: ApprovalStates.ContractConfirmed,
        name: 'Contract Confirmed/Declined',
        icon: 'playlist_add_check',
        states: approvalStates.filter(state => state.value === 3 || state.value === 4)
      },
    ]
    const currentStep: Ref = ref(undefined)
    const type: Ref<number|null> = ref(null)
    const selected: Ref<number|null> = ref(null)

    return {
      show: ref(true),
      removed: ref(false),
      date: ref(dateTime),
      type: type,
      timeout,
      statuses,
      info: '',
      currentStep,
      approvalStates,
      selected,
      steps: steps
    }
  },
  computed: {
    currentsteps() {
      if (!this.mailStore.mails.has(this.student.id)) return []
      const data = (this.mailStore.mails.get(this.student.id) ?? []).filter(mail => mail.type !== null)
      if (!this.currentStep) {
        this.currentStep = this.statuses.find(s => !data.map(d=> d.type ).includes(s))
      }
      return data
    },
    currentstepids() {
      return this.currentsteps.map(
        mail => {
          const type = mail.type
          if (type === 2 || type === 5) return 2
          if (type === 3 || type === 4) return 3
          return type
        }
      )
    },
  },
  async mounted() {
    await this.mailStore.getMails(this.student)
  },
  methods: {
    adaptState(newState: any, oldState: any) {
      this.selected = this.steps.filter(step => step.state === newState)[0].states[0].value
    },
    async deleteMail(mail: Mail) {
      await this.mailStore.deleteMail(mail)
      await this.mailStore.getMails(this.student)
    },
    onclickmail() {
      if (this.selected !== null) {
        this.type = this.selected

        const label = approvalStates.filter(state => state.value === this.selected)[0].label
        if (this.info) this.info = label + ': ' + this.info
        else this.info = label

        this.sendMail();
        if (this.currentStep) this.currentStep++;
      }
    },
    async sendMail() {
      await this.mailStore.sendMail(this.student, this.type, this.date, this.info)
      await this.mailStore.getMails(this.student)

      this.reset()
    },
    reset() {
      this.type = null
      this.date = (new Date()).toLocaleString()
      this.info = ''
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


