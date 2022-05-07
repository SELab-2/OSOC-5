<template>
  <q-card style="min-width: 350px">
    <q-card-section horizontal>
      <q-card-section class="col-3 flex flex-center">
        <q-icon name="warning" class="text-red" size="80px" />
      </q-card-section>
      <q-card-section class="q-pt-xs">
        <div class="text-h6 q-mt-sm q-mb-xs">
          Are you sure you want to delete "{{ deleteProjectName }}"?
        </div>
        <div class="text text-grey">
          This project will be deleted immediately and all coaches and skills
          will be removed. You cannot undo this action.
        </div>
        <br>
        <q-input
          v-model="deleteConfirm"
          outlined
          autofocus
          label="Project name"
          class="inputfield"
          :rules="[
            (val) =>
              (val && val.length > 0 && val === deleteProjectName) ||
              'Confirm the project name to continue.',
          ]"
        />
      </q-card-section>
    </q-card-section>

    <q-card-actions align="right" class="text-primary">
      <btn v-close-popup flat color="grey" label="Cancel" />
      <btn
        :disabled="deleteConfirm !== deleteProjectName"
        v-close-popup
        flat
        color="red"
        label="Delete"
        @click="deleteProjectConfirm(deleteProjectId ?? -1)"
        glow-color="red-2"
      />
    </q-card-actions>
  </q-card>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'
import { useProjectStore } from '../../../../stores/useProjectStore'
import { ref } from "vue";
import router from "../../../../router";

export default defineComponent({
  props: {
    deleteProjectId: {
      type: Number,
      required: true,
    },
    deleteProjectName: {
      type: String,
      required: true,
    },
  },
  setup() {
    const projectStore = useProjectStore()
    const deleteConfirm = ref('')

    return {
      projectStore,
      deleteConfirm,
    }
  },
  methods: {
    deleteProjectConfirm(id: number) {
      if (id !== -1) {
        this.projectStore.deleteProject(
          id, // callback
          (success: boolean) => {
            if (success) {
              router.push('/projects')
              this.projectStore.loadProjects()
              this.$q.notify({
                icon: 'done',
                color: 'positive',
                message: 'Successfully deleted!',
              })
            } else {
              this.$q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Failed to delete, project is in use!',
              })
            }
          }
        )
      }
    },
  },
})
</script>
