<template>
    <!--TODO: maybe global margin instead of on each page-->
    <div style='margin: 5px'>
        <SideBar />
            <div class="q-ma-sm">
        <h class="text-bold text-h3 q-mx-sm" >Projects</h>
        
        
        <div class='row justify-start content-start'>
            <div v-for='(item, index) in [ {}, {}, {}, {}, {}, {}, {} ]' :key='index' class="col-sm-12 col-md-6 col-lg-4 col-xl-3">
            <q-card 
                    class='my-card shadow-4 q-ma-sm' flat bordered>

                <q-card-section>
                    <div class='row'>
                        <div class='col'>
                            <div class='text-h5 text-bold q-mt-sm q-mb-xs'>Project {{ index }}</div>
                            <div class='text-overline'>Client {{ index }}</div>
                        </div>
                        <div>
                            <q-btn flat round size="12px" color='primary' icon='mail' />
                            <q-btn flat round size="12px" color='primary' icon='info' />
                            <q-btn flat round size="12px" color='primary' icon='edit' />
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
                                <span class='text-grey-8 text-caption'>Frond End Developer</span>
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
            </div>

            <q-page-sticky position='top-right' :offset='[15, 10]'>
                <q-btn padding='7px' icon='warning' color='red' label='Conflicts'
                       to='/projects/conflicts' />
            </q-page-sticky>

            <q-page-sticky position='bottom-right' :offset='[18, 18]'>
                <q-btn fab padding="10px" icon='add' color='yellow' to='/projects/create' />
            </q-page-sticky>
        </div>
            </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import SideBar from '../tools/SideBar.vue'

export default {
    name: 'Projects.vue',

    components: {
        SideBar,
    },
}
</script>

<style scoped>

</style>

<style lang='sass' scoped>
.my-card
    border-radius: 10px !important
    
:deep(.q-btn--rectangle)
    border-radius: 12px !important

.q-btn
    margin: 5px
</style>