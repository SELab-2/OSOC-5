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
              outlined
              v-model="project_name"
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
              outlined
              v-model="project_partner_name"
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
              outlined
              v-model="project_link"
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
                outlined
                dense
                debounce="300"
                color="green"
                class="inputfield"
                v-model="filter_coaches"
                placeholder="Search"
                @keydown.enter.prevent=""
              >
                <template v-slot:append>
                  <q-icon
                    v-if="filter_coaches !== ''"
                    name="close"
                    @click="filter_coaches = ''"
                    class="cursor-pointer"
                  />
                  <q-icon v-if="filter_coaches === ''" name="search" />
                </template>
              </q-input>
            </div>
            <q-table
              class="table shadow-4"
              :rows="coachStore.users"
              :columns="columns_coaches"
              :loading="coachStore.isLoadingUsers"
              row-key="displayName"
              selection="multiple"
              v-model:selected="selected"
              :filter="filter_coaches"
              :pagination.sync="pagination_coaches"
            >
            </q-table>
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
                style="max-width: 190px"
                outlined
                dense
                debounce="300"
                color="green"
                class="inputfield"
                v-model="filter_roles"
                placeholder="Search"
                @keydown.enter.prevent=""
              >
                <template v-slot:append>
                  <q-icon
                    v-if="filter_roles !== ''"
                    name="close"
                    @click="filter_roles = ''"
                    class="cursor-pointer"
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
              <template v-slot:body="props">
                <q-tr
                  :class="props.rowIndex % 2 === 1 ? 'bg-green-1' : ''"
                  :props="props"
                >
                  <q-td key="role" :props="props"> {{ props.row.name }}</q-td>
                  <q-td key="amount" :props="props">
                    {{ props.row.amount }}
                    <q-popup-edit
                      v-model.number="props.row.amount"
                      buttons
                      label-set="Save"
                      label-cancel="Close"
                      :validate="amountRangeValidation"
                      @hide="amountRangeValidation"
                      v-slot="scope"
                    >
                      <q-input
                        type="number"
                        v-model.number="scope.value"
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
                      buttons
                      v-model="props.row.comment"
                      v-slot="scope"
                    >
                      <q-input
                        type="text"
                        autogrow
                        v-model="scope.value"
                        autofocus
                        counter
                        borderless
                        @keyup.enter.stop
                      />
                    </q-popup-edit>
                  </q-td>
                  <q-td style="width: 10px" key="remove">
                    <q-btn
                      flat
                      round
                      style="color: #f14a3b"
                      @click="
                        delete_role = props.row.id
                        delete_role_prompt = true
                      "
                      icon="mdi-trash-can-outline"
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
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Create a new role</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input
          outlined
          autofocus
          v-model="new_role"
          class="inputfield"
          label="Role name"
          lazy-rules
          :rules="[
            (val) =>
              (val && val.length > 0) || 'Enter the name of the new role.',
          ]"
        />
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="Cancel" v-close-popup />
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
        <q-btn flat color="grey" label="Cancel" v-close-popup />
        <q-btn flat color="red" label="Delete" @click="delete_role_confirm" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import router from '../../router'
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { onMounted } from '@vue/runtime-core'
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'

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
    name: 'action',
    align: 'right',
    label: '',
    field: '',
    sortable: false,
  },
]

const columns_coaches = [
  /* TODO: Could display existing projects of coaches  */
  {
    name: 'displayName',
    align: 'left',
    label: 'Coach name',
    field: (row) => row.firstName + ' ' + row.lastName,
    sortable: true,
  },
]

export default {
  setup() {
    const skillStore = useSkillStore()
    const coachStore = useCoachStore()

    onMounted(() => {
      skillStore.loadSkills()
      coachStore.loadUsers()
    })

    const $q = useQuasar()

    // input fields
    const project_name = ref(null)
    const project_partner_name = ref(null)
    const project_link = ref(null)

    // Role amount error handling
    const errorRoleAmount = ref(false)
    const errorMessageRoleAmount = ref('')

    // Filters
    const filter_roles = ref('')
    const filter_coaches = ref('')

    // variables for the new role dialog popup
    const new_role_prompt = ref(false)
    const new_role = ref('')

    // variables for the delete role dialog popup
    const delete_role_prompt = ref(false)
    const delete_role = ref(-1)

    const selected = ref([])

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

      selected,
      columns_roles,
      columns_coaches,

      /*
       * Form Functions
       */
      onSubmit() {
        console.log(selected.value)

        let selected_coaches = [] // TODO selection is broken

        skillStore.submitProject(
          project_name.value,
          project_link.value,
          project_partner_name.value,
          selected_coaches,
          (success) => {
            if (success) {
              router.push('/projects/')

              $q.notify({
                icon: 'done',
                color: 'positive',
                message: 'Submitted',
              })
            } else {
              $q.notify({
                icon: 'close',
                color: 'negative',
                message: 'Failed',
              })
            }
          }
        )
      },
      onReset() {
        project_name.value = null
        project_partner_name.value = null
        project_link.value = null
        /* TODO expand if actually used ... */
      },

      /*
       * Role amount validation
       */
      errorRoleAmount,
      errorMessageRoleAmount,
      amountRangeValidation(val) {
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
          message: 'Deleted',
        })
      },

      /*
       * New Role
       */
      new_role_prompt,
      new_role,
      new_role_confirm() {
        // check if the new role value is valid
        if (new_role.value && new_role.value.length > 0) {
          // when valid call the store object and add the skill
          skillStore.addSkill(
            new_role.value,
            // callback
            (success) => {
              if (success) {
                new_role_prompt.value = false
                new_role.value = ''
                $q.notify({
                  icon: 'done',
                  color: 'warning',
                  message: `Added new project role: ${new_role.value}!`,
                  textColor: 'black',
                })
              } else {
                $q.notify({
                  icon: 'close',
                  color: 'negative',
                  message: 'Failed to add',
                })
              }
            }
          )
        }
      },
    }
  },
}
</script>

<style>
thead {
  background-color: #44dba4;
}

.q-card {
  border-radius: 10px !important;
}
</style>
<style scoped lang="sass">

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
