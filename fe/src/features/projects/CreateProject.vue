<template>
    <q-form
        class='createProjectForm'
        @submit='onSubmit'
        @reset='onReset'
        window-height window-width row justify-center items-center
    >

        <div class='row wrap justify-center items-baseline content-start'>
            <div class='projectcol basiccol items-center col-xs-12 col-sm-6 col-md-4 col-lg-3 col-xl-3'>
                <div class='text-bold text-h4'> Create project</div>
                <h4 class='projectsubtitle'>Basic Info</h4>
                <q-input
                    outlined
                    v-model='project_name'
                    label='Project name'
                    lazy-rules
                    class='inputfield'
                    :rules="[ (val) => (val && val.length > 0) || 'Please enter the name of the project.', ]"
                />
                <q-input
                    outlined
                    v-model='project_partner_name'
                    label='Partner name'
                    lazy-rules
                    class='inputfield'
                    :rules="[ (val) => (val && val.length > 0) || 'Please enter the name of the partner.', ]"
                />
                <q-input
                    outlined
                    v-model='project_link'
                    label='Project URL'
                    lazy-rules
                    class='inputfield'
                    type='URL'
                    :rules="[ (val) => (val && val.length > 0) || 'Please enter the URL of the project.', ]"
                />
            </div>

            <div class='projectcol coachescol items-center col-xs-12 col-sm-6 col-md-5 col-lg-3 col-xl-3'>
                <div class='text-bold text-h4'>⠀⠀</div>
                <h4 class='projectsubtitle'>Project Coaches</h4>
                <div class='row'>
                    <q-input
                        outlined
                        dense
                        debounce='300'
                        color='green'
                        class='inputfield'
                        v-model='filter_coaches'
                        placeholder='Search'
                    >
                        <template v-slot:append>
                            <q-icon v-if="filter_coaches !== ''"
                                    name='close'
                                    @click="filter_coaches = ''"
                                    class='cursor-pointer'
                            />
                            <q-icon v-if="filter_coaches === ''" name='search' />
                        </template>
                    </q-input>
                </div>
                <q-table
                    class='table shadow-4'
                    :rows='rows_coaches'
                    :columns='columns_coaches'
                    row-key='name'
                    selection='multiple'
                    v-model:selected='selected'
                    :filter='filter_coaches'
                    :pagination.sync='pagination_coaches'
                >
                </q-table>
            </div>

            <div class='projectcol rolescol items-center col-xs-12 col-sm-12 col-md-8 col-lg-6 col-xl-6'>
                <div class='text-bold text-h4'>⠀⠀</div>
                <h4 class='projectsubtitle'>Project Roles</h4>
                <div class='row'>
                    <q-btn class='cornered' color='primary' icon='add' label='Add role'
                           @click='new_role_prompt = true ' />
                    <q-space />
                    <q-input
                        outlined
                        dense
                        debounce='300'
                        color='green'
                        class='inputfield'
                        v-model='filter_roles'
                        placeholder='Search'
                    >
                        <template v-slot:append>
                            <q-icon v-if="filter_roles !== ''"
                                    name='close'
                                    @click="filter_roles = ''"
                                    class='cursor-pointer'
                            />
                            <q-icon v-if="filter_roles === ''" name='search' />
                        </template>
                    </q-input>
                </div>
                <q-table
                    class='table shadow-4'
                    :rows='skillStore.skills'
                    :columns='columns_roles'
                    :loading="skillStore.isLoadingSkills"
                    :pagination.sync='pagination_roles'
                    row-key='name'
                    :filter='filter_roles'
                >
                    <template v-slot:body='props'>
                        <q-tr :class="props.rowIndex % 2 === 1 ? 'bg-green-1' : ''" :props='props'>
                            <q-td key='role' :props='props'> {{ props.row.name }}</q-td>
                            <q-td key='amount' :props='props'>
                                {{ props.row.amount }}
                                <q-popup-edit
                                    v-model.number='props.row.amount'
                                    buttons
                                    label-set='Save'
                                    label-cancel='Close'
                                    :validate='amountRangeValidation'
                                    @hide='amountRangeValidation'
                                    v-slot='scope'
                                >
                                    <q-input
                                        type='number'
                                        v-model.number='scope.value'
                                        hint='Enter a positive number.'
                                        :error='errorRoleAmount'
                                        :error-message='errorMessageRoleAmount'
                                        dense
                                        autofocus
                                        borderless
                                        @keyup.enter='scope.set'
                                    />
                                </q-popup-edit>
                            </q-td>
                            <q-td key='comment' :props='props'>
                                <div>{{ props.row.comment }}</div>
                                <q-popup-edit buttons
                                              v-model='props.row.comment'
                                              v-slot='scope'
                                >
                                    <q-input
                                        type='text'
                                        autogrow
                                        v-model='scope.value'
                                        autofocus
                                        counter
                                        borderless
                                        @keyup.enter.stop
                                    />
                                </q-popup-edit>
                            </q-td>
                        </q-tr>
                    </template>
                </q-table>

                <br />

                <div class='row'>
                    <q-space />
                    <q-btn
                        elevated
                        color='primary'
                        label='Cancel'
                        type='cancel'
                        size='md'
                        class='q-mx-md cornered'
                        to='/projects'
                    />
                    <q-btn
                        elevated
                        color='primary'
                        label='Submit'
                        type='submit'
                        size='md'
                        class='q-mx-md cornered'
                    />
                </div>

            </div>


        </div>

    </q-form>

    <q-dialog v-model='new_role_prompt' persistent>
        <q-card style='min-width: 350px'>
            <q-card-section>
                <div class='text-h6'>Create a new role</div>
            </q-card-section>

            <q-card-section class='q-pt-none'>
                <q-input outlined
                         autofocus
                         v-model='new_role'
                         class='inputfield'
                         label='Role name'
                         lazy-rules
                         :rules="[ (val) => (val && val.length > 0) || 'Enter the name of the new role.', ]"
                />
            </q-card-section>

            <q-card-actions align='right' class='text-primary'>
                <q-btn flat label='Cancel' v-close-popup />
                <q-btn flat label='Add role' @click='new_role_confirm' />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import { onMounted } from '@vue/runtime-core'
import { useSkillStore } from '../../stores/useSkillStore'

const columns_roles = [
    { name: 'role', align: 'left', label: 'Project Role', field: 'role' },
    { name: 'amount', align: 'center', label: 'Amount', field: 'amount' },
    { name: 'comment', align: 'left', label: 'Comment', field: 'comment' },
]

const columns_coaches = [ /* TODO: Could display existing projects of coaches  */
    { name: 'name', align: 'left', label: 'Coach name', field: 'name' },
]
const rows_coaches = [
    { name: 'Ed SheRan' },
    { name: 'Mario' },
    { name: 'Luise' },
    { name: 'Bob' },
    { name: 'Gunter' },
    { name: 'An' },
    { name: 'Domien' },
    { name: 'Florian' },
    { name: 'Kees' },
    { name: 'Gert' },
    { name: 'Joris' },
    { name: 'Frans' },
    { name: 'Geert' },
]

export default {
    setup() {
        const skillStore = useSkillStore()

        onMounted(() => {
            skillStore.loadSkills()

            skillStore.$subscribe((skills, state) => {
                // handle callback


            })
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



        return {
            $q,
            skillStore,

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

            selected: ref([]),
            coaches: ref([]),
            coaches_options: [
                { label: 'Ed Sheran', value: 'Sheran', color: 'yellow' },
                { label: 'Charlie', value: 'Charlie', color: 'yellow' },
                { label: 'Obama', value: 'Obama', color: 'yellow' },
                { label: 'James', value: 'James', color: 'yellow' },
                { label: 'Arthur', value: 'Arthur', color: 'yellow' },
            ],
            onSubmit() {
                $q.notify({
                    icon: 'done',
                    color: 'positive',
                    message: 'Submitted',
                })
            },
            onReset() {
                project_name.value = null
                project_partner_name.value = null
                project_link.value = null
                /* TODO expand if actually used ... */
            },

            columns_roles,
            columns_coaches,
            rows_coaches,

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

            new_role_prompt,
            new_role,
            new_role_confirm() {
                if (new_role.value && new_role.value.length > 0) {
                    skillStore.addSkill(
                        new_role.value,
                        (added_role) => {
                            new_role_prompt.value = false
                            new_role.value = ''
                            return $q.notify({
                                icon: 'done',
                                color: 'warning',
                                message: `Added new project role: ${added_role}!`,
                                textColor: 'black',
                            })
                        })

                }
            },
        }
    },
}

</script>

<style>
thead {
    background-color: #44DBA4
}

</style>
<style scoped lang='sass'>

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
    margin: 25px

.appPageTitle
    text-align: center

.basiccol
    max-width: 360px !important

.rolescol
    max-width: 700px !important

.coachescol
    max-width: 360px !important

</style>
