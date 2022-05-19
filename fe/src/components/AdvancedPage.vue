<template>
  <div class="q-pt-lg flex relative-position justify-center">
    <div>
      <div class="text-bold text-h4">Advanced options</div>
      <div class="row">
        <div class="column">
          <div class="text-bold text-h5">Bulk deletion</div>
          <div class="row">Select items to be deleted:</div>
          <q-checkbox
            v-for="title in Object.keys(items)"
            :key="title"
            v-model="deleteItems"
            color="red"
            size="md"
            :val="title"
            :label="title"
          />
          <div class="row">
            <q-btn
              color="red"
              icon="mdi-trash-can-outline"
              icon-right="send"
              label="DELETE"
              :disable="deleteItems.length === 0"
              @click="display_popup = true"
            />
          </div>
        </div>
        <q-separator vertical spaced inset />
        <div class="column">
          <div class="text-bold text-h5">Download CSV</div>
          <div class="column q-gutter-sm">
            <q-btn
              v-for="(csv, title) in items"
              :key="title"
              color="primary"
              style="width: 200px"
              icon-right="archive"
              :label="title + ' (csv)'"
              no-caps
              @click="() => getCSV(title, csv)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>

  <q-dialog v-model="display_popup" persistent>
    <q-card style="min-width: 350px">
      <q-card-section horizontal>
        <q-card-section class="col-3 flex flex-center">
          <q-icon name="warning" class="text-red" size="80px"/>
        </q-card-section>
        <q-card-section class="q-pt-xs">
          <div class="text-h6 q-mt-sm q-mb-xs">Are you sure?</div>
          <div class="text text-grey">
            This will delete all '{{ deleteItems.join(', ') }}' immediately. You
            cannot undo this action.
          </div>
          <br/>
          <div v-for="item in deleteItems" :key="item">
            Type 'DELETE {{ item.toUpperCase() }}' in the field below to
            confirm.
            <q-input
              v-model="deleteConfirmItems[item]"
              outlined
              autofocus
              class="inputfield"
              :rules="[
                (val) =>
                  (val &&
                    val.length > 0 &&
                    val === `DELETE ${item.toUpperCase()}`) ||
                  `Input does not equal 'DELETE ${item.toUpperCase()}'!`,
              ]"
            />
          </div>
        </q-card-section>
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <btn v-close-popup flat color="grey" label="Cancel"/>
        <btn
          flat
          color="red"
          label="Delete"
          glow-color="red-2"
          @click="deleteSelected"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import {ref} from 'vue'
import {useStudentStore} from '../stores/useStudentStore'
import {instance} from '../utils/axios'
import {useProjectStore} from "../stores/useProjectStore";
import {useSkillStore} from "../stores/useSkillStore";
import {useCoachStore} from "../stores/useCoachStore";
import {useMailStore} from "../stores/useMailStore";
import {exportFile} from 'quasar';

export default {
  setup() {
    return {
      deleteItems: ref([]),
      display_popup: ref(false),
      deleteConfirm: ref(''),
      deleteConfirmItems: ref({}),
    }
  },
  data() {
    const studentStore = useStudentStore()
    const mailStore = useMailStore()
    const coachStore = useCoachStore()
    const projectStore = useProjectStore()
    const skillStore = useSkillStore()

    const items = {
      'Students': async () => studentStore.csv(),
      'Emails': async () => mailStore.csv(),
      'Coaches': async () => coachStore.csv(),
      'Projects': async () => projectStore.csv(),
      'Skills': async () => skillStore.csv()
    }

    return {
      items
    }
  },
  methods: {
    async getCSV(title: string, csv: Function) {
      const data = await csv()
      exportFile(title.toLowerCase() + (new Date).toLocaleString() + '.zip', data.data, data.headers)
    },
    checkIfValid() {
      // @ts-ignore
      for (const item of this.deleteItems) {
        // @ts-ignore
        if (`DELETE ${item.toUpperCase()}` !== this.deleteConfirmItems[item]) {
          return false
        }
      }
      return true
    },
    deleteSelected() {
      if (this.checkIfValid()) {
        // @ts-ignore
        console.log(this.deleteItems)
        // @ts-ignore
        for (const item of this.deleteItems) {
          instance.delete(`${item.toLowerCase()}/delete_all`)
          // console.log(`${item.toLowerCase()}/delete_all`)
        }
        // @ts-ignore
        this.$q.notify({
          icon: 'done',
          color: 'positive',
          // @ts-ignore
          message: `Deleted ${this.deleteItems.join(', ')} successfully!`,
        })
        // @ts-ignore
        this.display_popup = false
        // @ts-ignore
        this.deleteItems = []
        // @ts-ignore
        this.deleteConfirm = ''
        // @ts-ignore
        this.deleteConfirmItems = {}
      } else {
        // @ts-ignore
        this.$q.notify({
          icon: 'warning',
          color: 'negative',
          message: `Error: confirmation field(s) are not valid!`,
          textColor: 'black'
        });
      }
    },
  }
}
</script>
<style lang="sass">
.q-field__bottom
  margin-bottom: 3px
</style>
