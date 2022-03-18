<template>
    <div class='q-pa-md'>
        <q-page-container>
            <h class='text-bold text-h4'> Projects</h>

            <q-page-sticky position='bottom-right' :offset='[18, 18]'>
                <q-btn
                    fab
                    icon='add'
                    color='accent'
                    to='/projects/create'
                />
            </q-page-sticky>
        </q-page-container>
    </div>
</template>

<script>
export default {
    name: 'Projects.vue',
}
</script>

<style scoped>

</style>