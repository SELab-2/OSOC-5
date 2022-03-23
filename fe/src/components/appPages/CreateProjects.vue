<template>
    <q-form
        @submit='onSubmit'
        @reset='onReset'
        style='max-width: 90%; margin: 25px auto'
    >
        <h2 style='font-weight: 800'>Create project</h2>
        <div class='row'>
            <div class='projectcol col-xs-12 col-sm-12 col-md-6 col-lg-4'>
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

            <div class='projectcol col-xs-12 col-sm-12 col-md-6 col-lg-4'>
                <h4 class='projectsubtitle'>Project Roles</h4>
                <q-table
                    class='table shadow-4'
                    :rows='rows_rols'
                    :columns='columns_roles'
                    :pagination.sync='pagination_roles'
                    row-key='name'
                    :filter='filter_roles'
                >
                    <template v-slot:top>
                        <q-btn color='primary' icon='add' label='Add role'
                               @click='new_role_prompt = true ' />
                        <q-space />
                        <q-input
                            outlined
                            dense
                            debounce='300'
                            color='yellow-4'
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
                    </template>
                    <template v-slot:body='props'>
                        <q-tr :class="props.rowIndex % 2 === 1 ? 'bg-yellow-1' : ''" :props='props'>
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
                                        type='textarea'
                                        v-model='scope.value'
                                        autofocus
                                        counter
                                        @keyup.enter.stop
                                    />
                                </q-popup-edit>
                            </q-td>
                        </q-tr>
                    </template>
                </q-table>


            </div>

            <div class='projectcol col-xs-12 col-sm-12 col-md-6 col-lg-4'>
                <h4 class='projectsubtitle'>Project Coaches</h4>
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
                    <template v-slot:top>
                        <q-input
                            outlined
                            dense
                            debounce='300'
                            color='yellow-4'
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
                    </template>
                </q-table>
            </div>

        </div>

        <br />

        <div class='coachesrow row'>
            <q-space />
            <q-btn
                unelevated
                color='primary'
                label='Cancel'
                type='cancel'
                size='md'
                class='q-mx-md cornered primarybuttonshadow'
                to='/projects'
            />
            <q-btn
                unelevated
                color='primary'
                label='Submit'
                type='submit'
                size='md'
                class='q-mx-md cornered primarybuttonshadow'
            />
            <q-space />
        </div>
    </q-form>

    <q-dialog v-model='new_role_prompt' persistent>
        <q-card style='min-width: 350px'>
            <q-card-section>
                <div class='text-h6'>Enter new role name:</div>
            </q-card-section>

            <q-card-section class='q-pt-none'>
                <q-input dense v-model='new_role' autofocus
                         @keyup.enter='new_role_prompt = false' />
            </q-card-section>

            <q-card-actions align='right' class='text-primary'>
                <q-btn flat label='Cancel' v-close-popup />
                <q-btn flat label='Add role' v-close-popup />
                <!--                TODO: this doesn't add it to the list yet-->
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref } from 'vue'

const columns_roles = [
    { name: 'role', align: 'left', label: 'Project Role', field: 'role' },
    { name: 'amount', align: 'center', label: 'Amount', field: 'amount' },
    { name: 'comment', align: 'left', label: 'Comment', field: 'comment' },
]

const rows_rols = [
    {
        name: 'Frond-End',
        amount: 0,
        comment: 'Must know react.',
    },
    {
        name: 'Back-End',
        amount: 0,
        comment: '',
    },
    {
        name: 'Data Engineer',
        amount: 0,
        comment: '',
    },
    {
        name: 'Research',
        amount: 0,
        comment: '',
    },
    {
        name: 'Comms',
        amount: 0,
        comment: '',
    },
    {
        name: 'Full Stack Developer',
        amount: 0,
        comment: '',
    },
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
        const $q = useQuasar()
        const project_name = ref(null)
        const project_partner_name = ref(null)
        const project_link = ref(null)

        const errorRoleAmount = ref(false)
        const errorMessageRoleAmount = ref('')
        const filter_roles = ref('')
        const filter_coaches = ref('')

        const new_role_prompt = ref(false)
        const new_role = ref('')


        return {
            pagination_roles: {
                rowsPerPage: 10, // current rows per page being displayed
            },
            pagination_coaches: {
                rowsPerPage: 10, // current rows per page being displayed
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


            rows_rols: ref(rows_rols),
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
            addNewRole() {
                /* TODO: implement and use */
            },
        }
    },
}

</script>

<style scoped lang='sass'>

:deep(.q-field__control)
    border-radius: 14px !important
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px


.primarybuttonshadow
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px


.cornered
    border-radius: 10px !important


.projectcol
    padding-left: 15px
    padding-right: 15px

.projectsubtitle
    font-weight: 300
    text-align: center


.table
    border-radius: 10px

    thead
        /* bg color is important for th; just specify one */
        background-color: $yellow-7

</style>
