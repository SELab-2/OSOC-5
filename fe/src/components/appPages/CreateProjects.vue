<template>
    <q-form
        @submit='onSubmit'
        @reset='onReset'
        class='q-px-xl q-mb-xs'
        style='text-align: center; max-width: 80%; margin: 0 auto'
    >
        <h2 style='font-weight: 800'>Create project</h2>

        <div class='row'>
            <div class='col'>
                <h4 style='font-weight: 300'>Basic Info</h4>
                <q-input
                    outlined
                    v-model='project_name'
                    label='Project name'
                    lazy-rules
                    class='inputfield'
                    :rules="[
        (val) => (val && val.length > 0) || 'Please enter the name of the project.',
      ]"
                />
                <q-input
                    outlined
                    v-model='project_partner_name'
                    label='Partner name'
                    lazy-rules
                    class='inputfield'
                    :rules="[
        (val) => (val && val.length > 0) || 'Please enter the name of the partner.',
      ]"
                />
                <q-input
                    outlined
                    v-model='project_link'
                    label='Project link'
                    lazy-rules
                    class='inputfield'
                    type='URL'
                    :rules="[
        (val) => (val && val.length > 0) || 'Please enter the URL of the project.',
      ]"
                />
            </div>

            <div class='col'>
                <h4 style='font-weight: 300'>Project Roles</h4>
                * Insert list of roles *
                <!--TODO-->
            </div>

            <div class='col'>
                <h4 style='font-weight: 300'>Project Coaches</h4>
                * Insert list of coaches *
                <!--TODO-->
            </div>

        </div>

        <br />

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
    </q-form>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref } from 'vue'

export default {
    setup() {
        const $q = useQuasar()
        const project_name = ref(null)
        const project_partner_name = ref(null)
        const project_link = ref(null)
        return {

            project_name,
            project_partner_name,
            project_link,
            onSubmit() {
                $q.notify({
                    icon: 'done',
                    color: 'positive',
                    message: 'Submitted',
                })
            },
            onReset() {
                project_name.value = null
            },
        }
    },
}
</script>

<style scoped>

:deep(.q-field__control) {
    border-radius: 14px !important;
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}
</style>

<style>

.primarybuttonshadow {
    box-shadow: 0 5px 20px -4px #57bf98;
}

.cornered {
    border-radius: 10px !important;
}

.fpwd {
    float: right;
    position: absolute;
    top: 250px;
    right: 50px;
    font-size: 80%;
}
</style>
