<template>
    <h2 style='font-weight: 800'>Projects</h2>
    <div class='q-pa-md row items-start q-gutter-md'>
        <q-card class='my-card' flat bordered>

            <q-card-section>
                <div class='text-overline text-orange-9'>Client 1</div>
                <div class='text-h5 q-mt-sm q-mb-xs'>Project 1</div>
                <div class='text-caption text-grey'>Coach #1</div>
                <div class='text-caption text-grey'>Coach #2</div>
            </q-card-section>

            <q-card-actions>
                <q-btn flat color='dark' label='Edit' />
                <q-btn flat color='primary' label='Mail' />

                <q-space />

                <q-btn
                    color='grey'
                    round
                    flat
                    dense
                    :icon="expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                    @click='expanded = !expanded'
                />
            </q-card-actions>

            <q-slide-transition>
                <div v-show='expanded'>
                    <q-separator />
                    <q-card-section class='text-subitle2'>
                        {{ lorem }}
                    </q-card-section>
                </div>
            </q-slide-transition>
        </q-card>
        <q-page-sticky position='bottom-right' :offset='[18, 18]'>
            <q-btn fab icon='add' color='accent' to='/projects/create' />
        </q-page-sticky>
    </div>
</template>

<script>
import { ref } from 'vue'

export default {

    name: 'Projects.vue',
    setup() {
        return {
            expanded: ref(false),
            lorem: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        }
    },
}
</script>

<style scoped>

</style>

<style lang='sass' scoped>
.my-card
    width: 100%
    max-width: 350px
</style>