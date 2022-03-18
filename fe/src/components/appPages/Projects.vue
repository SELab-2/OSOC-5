<template>
    <h2 style='font-weight: 800'>Projects</h2>
    <div class='q-pa-md row items-start q-gutter-md'>


        <q-card  v-for="(item, index) in [ {}, {}, {}, {}, {}, {}, {} ]" :key="index" class='my-card' flat bordered>

            <q-card-section>
                <div class='text-h5 q-mt-sm q-mb-xs'>Project 1</div>
                <div class='text-overline '>Client 1</div>
                <div class='text-caption text-grey'>Coaches: Miet, Astrid</div>

            </q-card-section>
            <q-list bordered class='rounded-borders' style='max-width: 600px'>

<!--    LIJST VAN STUDENTEN            -->

                <q-item-label header>Students:</q-item-label>


                <q-item>
                    <q-item-section top>
                        <q-item-label lines='1'>
                            <span class='text-weight-medium'>Dayana Stark</span>
                        </q-item-label>
                        <span class='text-grey-8'>Frond End Developer</span>
                        <q-item-label caption lines='1'>
                            Suggested by <span class='text-weight-medium'>Jeroen Dewelde</span>
                        </q-item-label>
                    </q-item-section>

                    <q-item-section top side>
                        <div class='text-grey-8 q-gutter-xs'>
                            <q-btn class='gt-xs' size='12px' flat dense round icon='comment' />
                            <q-btn class='gt-xs' size='12px' flat dense round icon='info' />
                            <q-btn class='gt-xs' size='12px' flat dense round icon='delete' />
                        </div>
                    </q-item-section>
                </q-item>
                <q-separator spaced />

                <q-item>
                    <q-item-section top>
                        <q-item-label lines='1'>
                            <span class='text-weight-medium'>Dayana Stark</span>
                        </q-item-label>
                        <span class='text-grey-8'>Frond End Developer</span>
                        <q-item-label caption lines='1'>
                            Suggested by <span class='text-weight-medium'>Jeroen Dewelde</span>
                        </q-item-label>
                    </q-item-section>

                    <q-item-section top side>
                        <div class='text-grey-8 q-gutter-xs'>
                            <q-btn class='gt-xs' size='12px' flat dense round icon='comment' />
                            <q-btn class='gt-xs' size='12px' flat dense round icon='info' />
                            <q-btn class='gt-xs' size='12px' flat dense round icon='delete' />
                        </div>
                    </q-item-section>
                </q-item>
                <!--                <q-separator spaced />-->
            </q-list>

            <q-card-actions>
                <q-btn flat color='primary' label='Mail' />
                <q-space />
                <q-btn flat color='dark' label='Edit' />

            </q-card-actions>

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
}
</script>

<style scoped>

</style>

<style lang='sass' scoped>
.my-card
    width: 100%
    max-width: 400px
</style>