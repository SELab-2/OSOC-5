<template>
  <q-dialog
    class="full-width"
    :model-value="show"
    @update:model-value="() => resetDeleteRole()"
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
            Are you sure you want to delete "{{ deleteRole?.name }}"?
          </div>
          <div class="text text-grey">
            This skill will be deleted immediately from all projects. You can't
            undo this action.
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
          @click="deleteRoleConfirm(deleteRole?.id ?? -1)"
          glow-color="red-2"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {useSkillStore} from "../../../../stores/useSkillStore";

export default defineComponent ({
  props: {
    show: {
      type: Boolean,
      required: true
    },
    deleteRole: {
      type: Object,
      required: true
    },
    resetDeleteRole: {
      type: Function,
      required: true
    }
  },
  setup() {
    const skillStore = useSkillStore()

    return {
      skillStore
    }
  },
  methods: {
    deleteRoleConfirm(id: number) {
      if (id !== -1) {
        this.skillStore.deleteSkill(id).then(() => {
          this.resetDeleteRole()

          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Successfully deleted!',
          })
        })
      }
    },
  }
})
</script>
