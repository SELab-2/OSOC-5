<template>
  <div style="align-items: center; justify-content: center">
    <q-form class="createProjectForm" @submit="onSubmit" @reset="onReset">
      <div>
        <div class="row justify-between items-center q-gutter-sm">
          <div class="text-bold text-h4 projectcol">Create project</div>
          <div>
            <div class="q-gutter-sm">
              <q-btn
                elevated
                color="primary"
                label="Cancel"
                type="cancel"
                size="md"
                class="q-mx-md cornered"
                to="/projects"
              />
              <q-btn
                elevated
                color="primary"
                label="Submit"
                type="submit"
                size="md"
                class="q-mx-md cornered"
              />
            </div>
          </div>
        </div>
        <div class="row">
          <div
            class="projectcol col-xs-12 col-sm-12 col-md-6 col-lg-3 col-xl-3'"
          >
            <h4 class="projectsubtitle">Basic Info</h4>
            <q-input
              v-model="project_name"
              outlined
              label="Project name"
              lazy-rules
              class="inputfield"
              :rules="[
                (val) =>
                  (val && val.length > 0) ||
                  'Please enter the name of the project.',
              ]"
            />
            <q-input
              v-model="project_partner_name"
              outlined
              label="Partner name"
              lazy-rules
              class="inputfield"
              :rules="[
                (val) =>
                  (val && val.length > 0) ||
                  'Please enter the name of the partner.',
              ]"
            />
            <q-input
              v-model="project_link"
              outlined
              label="Project URL"
              lazy-rules
              class="inputfield"
              type="URL"
              :rules="[
                (val) =>
                  (val && val.length > 0) ||
                  'Please enter the URL of the project.',
              ]"
            />
          </div>

          <div
            class="projectcol col-xs-12 col-sm-12 col-md-6 col-lg-4 col-xl-3"
          >
            <h4 class="projectsubtitle">Project Coaches</h4>
            <div class="row">
              <q-input
                v-model="filter_coaches"
                outlined
                dense
                debounce="300"
                color="green"
                class="inputfield"
                placeholder="Search"
                @keydown.enter.prevent=""
              >
                <template #append>
                  <q-icon
                    v-if="filter_coaches !== ''"
                    name="close"
                    class="cursor-pointer"
                    @click="filter_coaches = ''"
                  />
                  <q-icon v-if="filter_coaches === ''" name="search" />
                </template>
              </q-input>
            </div>

            <q-table
              v-model:selected="selected_coaches"
              :pagination.sync="pagination_coaches"
              class="table shadow-4"
              :rows="coachStore.users"
              :columns="columns_coaches"
              :loading="coachStore.isLoadingUsers"
              row-key="url"
              selection="multiple"
              :filter="filter_coaches"/>
          </div>

          <div
            class="projectcol col-xs-12 col-sm-12 col-md-12 col-lg-5 col-xl-6"
          >
            <h4 class="projectsubtitle">Project Roles</h4>
            <div class="row">
              <q-btn
                class="cornered"
                color="primary"
                icon="add"
                label="Add role"
                @click="new_role_prompt = true"
              />
              <q-space />
              <q-input
                v-model="filter_roles"
                style="max-width: 190px"
                outlined
                dense
                debounce="300"
                color="green"
                class="inputfield"
                placeholder="Search"
                @keydown.enter.prevent=""
              >
                <template #append>
                  <q-icon
                    v-if="filter_roles !== ''"
                    name="close"
                    class="cursor-pointer"
                    @click="filter_roles = ''"
                  />
                  <q-icon v-if="filter_roles === ''" name="search" />
                </template>
              </q-input>
            </div>
            <q-table
              class="table shadow-4"
              :rows="skillStore.skills"
              :columns="columns_roles"
              :loading="skillStore.isLoadingSkills"
              :pagination.sync="pagination_roles"
              row-key="name"
              :filter="filter_roles"
            >
              <template #body="props">
                <q-tr
                  :class="props.rowIndex % 2 === 1 ? 'bg-green-1' : ''"
                  :props="props"
                >
                  <q-td key="role" :props="props">
                    {{ props.row.name }}
                  </q-td>
                  <q-td key="amount" :props="props">
                    {{ props.row.amount }}
                    <q-popup-edit
                      v-slot="scope"
                      v-model.number="props.row.amount"
                      buttons
                      label-set="Save"
                      label-cancel="Close"
                      :validate="amountRangeValidation"
                      @hide="amountRangeValidation"
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
                  <q-td key="comment" :props="props">
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
                  <q-td key="color" :props="props" auto-width>
                    <div
                      :style="`height: 25px; width:25px; border-radius: 50%;background: ${props.row.color}`"
                    ></div>
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
                  <q-td key="remove" style="width: 10px">
                    <q-btn
                      flat
                      round
                      style="color: #f14a3b"
                      icon="mdi-trash-can-outline"
                      @click="
                        ;(delete_role = props.row.id) &&
                          (delete_role_prompt = true)
                      "
                    />
                  </q-td>
                </q-tr>
              </template>
            </q-table>
          </div>
        </div>
      </div>
    </q-form>
  </div>

  <q-dialog v-model="new_role_prompt" persistent>
    <q-card class="create-role-popup">
      <q-card-section>
        <div class="text-h6">Create a new role</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input
          v-model="new_role"
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
          v-model="new_role_color"
          outlined
          label="text color"
          class="inputfield"
          type="URL"
        />
        <!--  INFO if picker gives conversion issues use-->
        <!--  INFO https://quasar.dev/quasar-utils/color-utils#color-conversion-->
        <q-color
          v-model="new_role_color"
          no-header
          no-footer
          class="color-picker"
        />
      </q-card-section>
      <q-card-actions align="right" class="text-primary">
        <q-btn v-close-popup flat label="Cancel" />
        <q-btn flat label="Add role" @click="new_role_confirm" />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="delete_role_prompt" persistent>
    <q-card style="min-width: 350px">
      <q-card-section horizontal>
        <q-card-section class="col-3 flex flex-center">
          <q-icon name="warning" class="text-red" size="80px" />
        </q-card-section>
        <q-card-section class="q-pt-xs">
          <div class="text-h6 q-mt-sm q-mb-xs">
            Are you sure you want to delete "{{ delete_role.name }}"?
          </div>
          <div class="text text-grey">
            This skill will be deleted immediately from all projects. You can't
            undo this action.
          </div>
        </q-card-section>
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn v-close-popup flat color="grey" label="Cancel" />
        <q-btn flat color="red" label="Delete" @click="delete_role_confirm" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import router from '../../router'
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { defineComponent, onMounted } from '@vue/runtime-core'
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'
import { User } from '../../models/User'
const columns_roles = [
  {
    name: 'role',
    align: 'left',
    label: 'Project Role',
    field: 'role',
    sortable: true,
  },
  {
    name: 'amount',
    align: 'left',
    label: 'Amount',
    field: 'amount',
    sortable: true,
  },
  {
    name: 'comment',
    align: 'left',
    label: 'Comment',
    field: 'comment',
    sortable: true,
  },
  {
    name: 'color',
    align: 'center',
    label: 'Color',
    field: 'color',
    sortable: false,
  },
  {
    name: 'action',
    align: 'right',
    label: '',
    field: '',
    sortable: false,
  },
]

const columns_coaches = [
  {
    name: 'displayName',
    align: 'left',
    label: 'Coach name',
    field: (row: { firstName: string; lastName: string }) =>
      row.firstName + ' ' + row.lastName,
    sortable: true,
  },
]

export default defineComponent({
  setup() {
    const skillStore = useSkillStore()
    const coachStore = useCoachStore()

    onMounted(() => {
      skillStore.loadSkills()
      coachStore.loadUsers()
    })

    const $q = useQuasar()

    // input fields
    const project_name = ref('')
    const project_partner_name = ref('')
    const project_link = ref('')

    // Role amount error handling
    const errorRoleAmount = ref(false)
    const errorMessageRoleAmount = ref('')

    // Filters
    const filter_roles = ref('')
    const filter_coaches = ref('')

    // variables for the new role dialog popup
    const new_role_prompt = ref(false)
    const new_role = ref('')
    const new_role_color = ref('')

    // variables for the delete role dialog popup
    const delete_role_prompt = ref(false)
    const delete_role = ref(-1)

    const selected_coaches = ref([])

    return {
      skillStore,
      coachStore,

      pagination_roles: {
        rowsPerPage: 5, // current rows per page being displayed
      },
      pagination_coaches: {
        rowsPerPage: 5, // current rows per page being displayed
      },

      project_name,
      project_partner_name,
      project_link,

      filter_roles,
      filter_coaches,

      selected_coaches,
      columns_roles,
      columns_coaches,

      /*
       * Form Functions
       */
      onSubmit() {

        let selected_coaches_urls: Array<string> = []
        for(let coach of selected_coaches.value as User[]){
          selected_coaches_urls.push(coach.url)
        }

        skillStore.submitProject(
          project_name.value,
          project_link.value,
          project_partner_name.value,
          selected_coaches_urls,
          (success: boolean) => {
            if (success) {
              router.push('/projects')

              $q.notify({
                icon: 'done',
                color: 'positive',
                message: 'Project created successfully!',
              })
            } else {
              $q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Project creation failed',
              })
            }
          }
        )
      },

      /*
       * Role amount validation
       */
      errorRoleAmount,
      errorMessageRoleAmount,
      amountRangeValidation(val: number) {
        if (val < 0) {
          errorRoleAmount.value = true
          errorMessageRoleAmount.value = 'The value must be positive!'
          return false
        }
        errorRoleAmount.value = false
        errorMessageRoleAmount.value = ''
        return true
      },

      delete_role_prompt,
      delete_role,

      delete_role_confirm() {
        skillStore.deleteSkill(delete_role.value)
        delete_role_prompt.value = false
        delete_role.value = -1

        $q.notify({
          icon: 'done',
          color: 'positive',
          message: 'Successfully deleted!',
        })
      },

      /*
       * New Role
       */
      new_role_prompt,
      new_role,
      new_role_color,
      new_role_confirm() {
        // check if the new role value is valid
        if (
          new_role.value &&
          new_role.value.length > 0 &&
          new_role_color.value.length > 0
        ) {
          // when valid call the store object and add the skill
          skillStore.addSkill(
            new_role.value,
            new_role_color.value,
            // callback
            (success: boolean) => {
              if (success) {
                $q.notify({
                  icon: 'done',
                  color: 'positive',
                  message: `Added new project role: ${new_role.value}.`,
                  textColor: 'black',
                })
                new_role_prompt.value = false
                new_role.value = ''
                new_role_color.value = ''
              } else {
                $q.notify({
                  icon: 'close',
                  color: 'negative',
                  message: 'Failed to add role!',
                })
              }
            }
          )
        } else {
          $q.notify({
            icon: 'close',
            color: 'negative',
            message: 'Invalid name/color!',
          })
        }
      },

    }
  },
})
</script>

<style>
thead {
  background-color: #44dba4;
}
</style>
<style scoped lang="sass">
.create-role-popup
    width: 300px

.cornered
    border-radius: 10px !important


.projectcol
    padding-left: 15px
    padding-right: 15px

.projectsubtitle
    font-weight: 300
    margin-top: 10px
    margin-bottom: 15px
    font-size: x-large

.table
    border-radius: 10px
    margin-top: 10px

.createProjectForm
    margin-top: 25px
    margin-left: 10%
    margin-right: 10%

.appPageTitle
    text-align: center
</style>
