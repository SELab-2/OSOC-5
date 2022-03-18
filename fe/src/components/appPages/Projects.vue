<template>
    <h2 style='font-weight: 800'>Projects</h2>

    <div class='q-pa-md row items-start q-gutter-md'>

        <q-card v-for='(item, index) in [ {}, {}, {}, {}, {}, {}, {} ]' :key='index' class='my-card' flat bordered>

            <q-card-section>
                <div class="row">
                    <div class="col">
                        <div class='text-h5 q-mt-sm q-mb-xs'>Project {{ index }}</div>
                        <div class='text-overline '>Client {{ index }}</div>
                    </div>
                    <div class="col-md-auto">
                        <q-btn round outline color="black" icon="mail" />
                        <q-btn round outline color="black" icon="edit" />
                    </div>
                </div>
                <div class='text-caption text-grey'>Coaches:</div>
                <q-chip outline icon='person'>Astrid</q-chip>
                <q-chip outline icon='person'>Miet</q-chip>

                <div class='text-caption text-grey'>Roles:</div>
                <q-chip outline icon='info'>
                    <q-tooltip anchor='top middle' self='center middle'>
                        Must know everything
                    </q-tooltip>
                    1x Full Stack Developer
                </q-chip>
                <q-chip outline>
                    1x Comms
                </q-chip>
                <q-chip outline icon='info'>
                    <q-tooltip anchor='top middle' self='center middle'>
                        Must know React.js
                    </q-tooltip>
                    1x Front-end Developer
                </q-chip>
                <q-chip outline>
                    1x Media
                </q-chip>
                <q-chip outline>
                    1x Back-end Developer
                </q-chip>

            </q-card-section>
            <q-list bordered separator>

                <!--    LIJST VAN STUDENTEN            -->

                <q-item-label header>Students:</q-item-label>

                <div v-for='(item, index) in [ {}, {}, {}, {} ]' :key='index'>
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
                </div>
                <!--                <q-separator spaced />-->
            </q-list>

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
    border-radius: 10px !important
    width: 100%
    max-width: 375px

.q-btn
    margin: 5px
</style>