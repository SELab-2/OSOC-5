<template>
  <div
    class="relative-position container flex justify-center"
    style="width: 100vw"
  >
    <div
      class="q-pa-md q-gutter-md"
      style="width: 1000px"
    >
      <div class="text-bold text-h4">
        Advanced options
      </div>
      <div class="text-bold text-h5">
        Bulk deletion
      </div>
      <div class="row">
        Select items to be deleted:
      </div>
      <div class="row">
        <q-checkbox
          v-model="deleteItems"
          color="red"
          size="md"
          val="Coaches"
          label="Coaches"
        />
      </div>
      <div class="row">
        <q-checkbox
          v-model="deleteItems"
          color="red"
          size="md"
          val="Emails"
          label="Emails"
        />
      </div>
      <div class="row">
        <q-checkbox
          v-model="deleteItems"
          color="red"
          size="md"
          val="Projects"
          label="Projects"
        />
      </div>
      <div class="row">
        <q-checkbox
          v-model="deleteItems"
          color="red"
          size="md"
          val="Skills"
          label="Skills"
        />
      </div>
      <div class="row">
        <q-checkbox
          v-model="deleteItems"
          color="red"
          size="md"
          val="Students"
          label="Students"
        />
      </div>
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
  </div>
  <q-dialog
    v-model="display_popup"
    persistent
  >
    <q-card style="min-width: 350px">
      <q-card-section horizontal>
        <q-card-section class="col-3 flex flex-center">
          <q-icon
            name="warning"
            class="text-red"
            size="80px"
          />
        </q-card-section>
        <q-card-section class="q-pt-xs">
          <div class="text-h6 q-mt-sm q-mb-xs">
            Are you sure?
          </div>
          <div class="text text-grey">
            This will delete all '{{ deleteItems.join(', ') }}' immediately.
            You cannot undo this action.
          </div>
          <br>
          <div
            v-for="item in deleteItems"
            :key="item"
          >
            Type 'DELETE {{ item.toUpperCase() }}' in the field below to confirm.
            <q-input
              v-model="deleteConfirmItems[item]"
              outlined
              autofocus
              class="inputfield"
              :rules="[
                (val) =>
                  (val && val.length > 0 && val === `DELETE ${item.toUpperCase()}`) ||
                  `Input does not equal 'DELETE ${item.toUpperCase()}'!`,
              ]"
            />
          </div>
        </q-card-section>
      </q-card-section>

      <q-card-actions
        align="right"
        class="text-primary"
      >
        <btn
          v-close-popup
          flat
          color="grey"
          label="Cancel"
        />
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
import { ref } from 'vue'
import { instance } from "../utils/axios";

export default {
  setup() {
    return {
      deleteItems: ref([]),
      display_popup: ref(false),
      deleteConfirm: ref(''),
      deleteConfirmItems: ref({}),
    }
  },
  methods: {
    checkIfValid(){
      for(const item of this.deleteItems){
        if (`DELETE ${item.toUpperCase()}` !== this.deleteConfirmItems[item]){
          return false
        }
      }
      return true
    },
    deleteSelected(){
      if (this.checkIfValid()){
        console.log(this.deleteItems)
        for(const item of this.deleteItems){
          instance.delete(`${item.toLowerCase()}/delete_all`)
        }

        this.$q.notify({
          icon: 'done',
          color: 'positive',
          message: `Deleted ${this.deleteItems.join(', ')} successfully!`,
        })

        this.display_popup = false
        this.deleteItems = []
        this.deleteConfirm = ''
        this.deleteConfirmItems = {}

      } else {
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
