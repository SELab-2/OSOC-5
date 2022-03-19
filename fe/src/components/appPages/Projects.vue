<template>
    <!--TODO: maybe global margin instead of on each page-->
    <div style='margin: 5px'>
        <SideBar />
            <div class="q-ma-sm">
        <h class="text-bold text-h3 q-mx-sm" >Projects</h>
        
        
        <div class='row justify-start content-start'>
            <div v-for='project in projects' :key='project.id' class="col-sm-12 col-md-6 col-lg-4 col-xl-3">
            <q-card 
                    class='my-card shadow-4 q-ma-sm' flat bordered>

                <q-card-section>
                    <div class='row'>
                        <div class='col'>
                            <div class='text-h5 text-bold q-mt-sm q-mb-xs'>{{ project.title }}</div>
                            <div class='text-overline'>{{ project.client }}</div>
                        </div>
                        <div>
                            <q-btn flat round size="12px" color='primary' icon='mail' />
                            <q-btn flat round size="12px" color='primary' icon='info' />
                            <q-btn flat round size="12px" color='primary' icon='edit' />
                        </div>
                    </div>
                    <div class='text-caption text-grey'>Coaches:</div>
                    <q-chip v-for="coach in project.coaches" :key="coach.id" icon='person'>{{ coach.name }}</q-chip>

                    <div class='text-caption text-grey'>Roles:</div>
                    <q-chip
                        outline
                        :color="role.color + '-4'"
                        v-for="(role, index) in project.roles" 
                        :class="'bg-' + role.color + '-1'"
                        style="border-width: 1.5px;"
                        :style="'padding-left: ' + (role.info ? '2px' : '8px') + '; padding-right: 8px;'" :key="index">
                        <template v-slot:default>
                            <div class="row" style="display: flex; align-items: center">
                                <q-icon v-if="role.info" 
                                    name="info" 
                                    size="sm" 
                                    :color="role.color + '-6'"/>
                                <div style="color: black;" 
                                    :style="'padding-left: ' + (role.info ? '3px' : '0px')"
                                    >{{ role.label }}</div>
                                <div class="text-bold" 
                                    style="padding-left: 3px;" 
                                    :class="'text-' + role.color + '-8'" 
                                    >{{ role.amount }}</div>
                                <q-tooltip 
                                    v-if="role.info" 
                                    :class="'bg-' + role.color + '-2'" 
                                    class="text-black shadow-2" 
                                    anchor='bottom middle' 
                                    self='center middle'
                                    >{{ role.info }}</q-tooltip>
                            </div>
                        </template>
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
    data() {
        return {
            projects: [
                {
                    id: 1,
                    title: "Project #1",
                    client: "Client #1",
                    coaches: [
                        { id: 1, name: "Miet" },
                        { id: 2, name: "Astrid" }
                    ],
                    roles: [
                        { type: "fullstack", amount: 2, label: "Full-Stack dev", color: 'green', info: "Must know everything." },
                        { type: "comms", amount: 1, label: "Communication", color: 'purple' },
                        { type: "frontend", amount: 2, label: "Frontend dev", color: 'orange', info: "Must know React.js." },
                        { type: "media", amount: 2, label: "Media", color: 'red' },
                        { type: "backend", amount: 2, label: "Backend dev", color: 'blue' }
                    ]
                }
            ]
        }
    }
}
</script>

<style lang='sass' scoped>
.my-card
    border-radius: 10px !important
    
:deep(.q-btn--rectangle)
    border-radius: 12px !important

.q-btn
    margin: 5px
</style>