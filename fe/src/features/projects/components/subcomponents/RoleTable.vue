<template>
  <q-table
    class="table shadow-4"
    :rows="skillStore.skills"
    :columns="columnsRoles"
    :loading="skillStore.isLoadingSkills"
    row-key="name"
    :filter="filterRoles"
  >
    <template #body="props">
      <q-tr
        :class="props.rowIndex % 2 === 1 ? 'bg-green-1' : ''"
        :props="props"
      >
        <q-td
          key="role"
          :props="props"
        >
          {{ props.row.name }}
        </q-td>
        <q-td
          key="amount"
          :props="props"
        >
          {{ props.row.amount }}
          <q-popup-edit
            v-slot="scope"
            v-model.number="props.row.amount"
            buttons
            label-set="Save"
            label-cancel="Close"
            :validate="amountRangeValidation"
          >
            <q-input
              v-model.number="scope.value"
              type="number"
              hint="Enter a positive number."
              :error="errorRoleAmount"
              :error-message="errorMessageRoleAmount"
              dense
              autofocus
              borderless
              @keyup.enter="scope.set"
            />
          </q-popup-edit>
        </q-td>
        <q-td
          key="comment"
          :props="props"
        >
          <div>{{ props.row.comment }}</div>
          <q-popup-edit
            v-slot="scope"
            v-model="props.row.comment"
            buttons
          >
            <q-input
              v-model="scope.value"
              type="text"
              autogrow
              autofocus
              counter
              borderless
              @keyup.enter.stop
            />
          </q-popup-edit>
        </q-td>
        <q-td
          key="color"
          :props="props"
          auto-width
        >
          <div
            :style="`height: 25px; width:25px; border-radius: 50%;background: ${props.row.color}`"
          />
          <!-- TODO make this actually change in the database not locally-->
          <q-popup-edit
            v-slot="scope"
            v-model="props.row.color"
            buttons
          >
            <q-color
              v-model="scope.value"
              no-header
              no-footer
              class="color-picker"
              @keyup.enter.stop
            />
          </q-popup-edit>
        </q-td>
        <q-td
          key="remove"
          style="width: 10px"
        >
          <btn
            flat
            round
            style="color: #f14a3b"
            icon="mdi-trash-can-outline"
            glow-color="red-2"
            @click="deleteRole = props.row"
          />
        </q-td>
      </q-tr>
    </template>
  </q-table>
  <q-dialog
    v-model="newRolePrompt"
    persistent
  >
    <q-card class="create-role-popup">
      <q-card-section>
        <div class="text-h6">
          Create a new role
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input
          v-model="newRole"
          outlined
          autofocus
          class="inputfield"
          label="Role name"
          lazy-rules
          :rules="[
            (val) =>
              (val && val.length > 0) || 'Enter the name of the new role.',
          ]"
        />
      </q-card-section>
      <q-card-section class="q-pt-none">
        <!--        TODO REMOVE -->
        <q-input
          v-model="newRoleColor"
          outlined
          label="text color"
          class="inputfield"
          type="url"
        />
        <!--  INFO if picker gives conversion issues use-->
        <!--  INFO https://quasar.dev/quasar-utils/color-utils#color-conversion-->
        <q-color
          v-model="newRoleColor"
          no-header
          no-footer
          class="color-picker"
        />
      </q-card-section>
      <q-card-actions
        align="right"
        class="text-primary"
      >
        <btn
          v-close-popup
          flat
          label="Cancel"
          glow-color="#C0FFF4"
        />
        <btn
          flat
          label="Add role"
          @click="newRoleConfirm"
          glow-color="#C0FFF4"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <DeleteRoleDialog
    :show="showDelete"
    :delete-role="deleteRole"
    :reset-delete-role="deleteRole = undefined"
  />

</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import {Ref, ref} from "vue";
import { SkillInterface } from "../../../../models/Skill";
import {useSkillStore} from "../../../../stores/useSkillStore";
import columnsRoles from "../../../../models/ProjectRolesColumns";
import DeleteRoleDialog from "./DeleteRoleDialog.vue";

export default defineComponent ({
  components: { DeleteRoleDialog },
  setup() {
    const skillStore = useSkillStore()

    // Filters
    const filterRoles = ref('')

    // variables for the new role dialog popup
    const newRolePrompt = ref(false)
    const newRole = ref('')
    const newRoleColor = ref('')

    // Role amount error handling
    const errorRoleAmount = ref(false)
    const errorMessageRoleAmount = ref('')

    const deleteRole: Ref<SkillInterface | undefined> = ref()

    return {
      newRolePrompt,
      newRole,
      newRoleColor,
      skillStore,
      deleteRole,
      errorRoleAmount,
      errorMessageRoleAmount,
      filterRoles,
      columnsRoles
    }
  },
  computed: {
    showDelete(): boolean {
      return this.deleteRole !== undefined
    }
  },
  methods: {
    newRoleConfirm() {
      // check if the new role value is valid
      if (
        this.newRole &&
        this.newRole.length > 0 &&
        this.newRoleColor.length > 0
      ) {

        // when valid call the store object and add the skill
        this.skillStore.addSkill(
          this.newRole,
          this.newRoleColor,

          // callback
          (success: boolean) => {
            if (success) {
              this.$q.notify({
                icon: 'done',
                color: 'positive',
                message: `Added new project role: ${this.newRole}.`,
                textColor: 'black',
              })
              this.newRolePrompt = false
              this.newRole = ''
              this.newRoleColor = ''
            } else {
              this.$q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Failed to add role!',
              })
            }
          }
        )
      } else {
        this.$q.notify({
          icon: 'close',
          color: 'negative',
          message: 'Invalid name/color!',
        })
      }
    },
    amountRangeValidation(val: number) {
      if (val < 0) {
        this.errorRoleAmount = true
        this.errorMessageRoleAmount = 'The value must be positive!'
        return false
      }
      this.errorRoleAmount = false
      this.errorMessageRoleAmount = ''
      return true
    },
  }
})
</script>
