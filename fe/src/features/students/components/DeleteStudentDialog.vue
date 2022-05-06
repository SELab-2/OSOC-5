<template>
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
          Are you sure you want to delete "{{ name }}"?
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
        v-close-popup
        flat
        color="red"
        label="Delete"
        @click="executeDelete"
        glow-color="red-2"
      />
    </q-card-actions>
  </q-card>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { useStudentStore } from "../../../stores/useStudentStore";

export default defineComponent ({
  props: {
    delete: {
      type: Function,
      required: true
    },
    name: {
      type: String,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()

    return {
      studentStore
    }
  },
  methods: {
    executeDelete: async function () {
      await this.delete()
    },
  }
})
</script>
