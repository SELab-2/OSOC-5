<template>
    <div style='margin: 5px'>
        <SideBar />
            <div class="q-ma-sm">
        <div class="text-bold text-h3 q-mx-sm" >Projects</div>
        
        <div>
            <masonry-wall :items="projects" :ssr-columns="1" :column-width="320" :gap="0">
              <template #default="{ item, index }">
                <project-card :project="item"/>
              </template>
            </masonry-wall>

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
import ProjectCard from '../tools/ProjectCard.vue'

export default {
    name: 'Projects.vue',
    
    components: {
        SideBar, ProjectCard
    },
    computed() {
        return {
            
        }
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
                        { type: "backend", amount: 3, label: "Backend dev", color: 'blue' }
                    ],
                    students: [
                        { id: 1, name: "Friedrich Vandenberghe", role: "fullstack"},
                        { id: 2, name: "Lander Saerens", role: "frontend"},
                        { id: 3, name: "Simon Heemeryck", role: "backend"},
                        { id: 4, name: "Wouter Hennen", role: "frontend"},
                        { id: 5, name: "Lisa De Jonghe", role: "comms"},
                        { id: 6, name: "Henri Cattoire", role: "backend"},
                        { id: 7, name: "Lennart Veys", role: "backend"}
                    ]
                },
                {
                    id: 2,
                    title: "Project #2",
                    client: "Client #2",
                    coaches: [
                        { id: 1, name: "Miet" },
                        { id: 2, name: "Astrid" }
                    ],
                    roles: [
                        { type: "fullstack", amount: 2, label: "Full-Stack dev", color: 'green', info: "Must know everything." },
                        { type: "comms", amount: 1, label: "Communication", color: 'purple' },
                        { type: "frontend", amount: 2, label: "Frontend dev", color: 'orange', info: "Must know React.js." },
                        { type: "media", amount: 2, label: "Media", color: 'red' },
                        { type: "backend", amount: 3, label: "Backend dev", color: 'blue' }
                    ],
                    students: [
                        { id: 1, name: "Friedrich Vandenberghe", role: "fullstack"},
                        { id: 2, name: "Lander Saerens", role: "frontend"},
                        { id: 3, name: "Simon Heemeryck", role: "backend"},
                        { id: 4, name: "Wouter Hennen", role: "frontend"},
                        { id: 5, name: "Lisa De Jonghe", role: "comms"},
                        { id: 6, name: "Henri Cattoire", role: "backend"},
                        { id: 7, name: "Lennart Veys", role: "backend"}
                    ]
                },
                {
                    id: 3,
                    title: "Project #3",
                    client: "Client #3",
                    coaches: [
                        { id: 1, name: "Miet" },
                        { id: 2, name: "Astrid" }
                    ],
                    roles: [
                        { type: "fullstack", amount: 2, label: "Full-Stack dev", color: 'green', info: "Must know everything." },
                        { type: "comms", amount: 1, label: "Communication", color: 'purple' },
                        { type: "frontend", amount: 2, label: "Frontend dev", color: 'orange', info: "Must know React.js." },
                        { type: "media", amount: 2, label: "Media", color: 'red' },
                        { type: "backend", amount: 3, label: "Backend dev", color: 'blue' }
                    ],
                    students: [
                        { id: 1, name: "Friedrich Vandenberghe", role: "fullstack"},
                        { id: 2, name: "Lander Saerens", role: "frontend"},
                        { id: 3, name: "Simon Heemeryck", role: "backend"},
                        { id: 4, name: "Wouter Hennen", role: "frontend"},
                        { id: 5, name: "Lisa De Jonghe", role: "comms"},
                        { id: 6, name: "Henri Cattoire", role: "backend"},
                        { id: 7, name: "Lennart Veys", role: "backend"}
                    ]
                },
                {
                    id: 4,
                    title: "Project #3",
                    client: "Client #3",
                    coaches: [
                        { id: 1, name: "Miet" },
                        { id: 2, name: "Astrid" }
                    ],
                    roles: [
                        { type: "fullstack", amount: 2, label: "Full-Stack dev", color: 'green', info: "Must know everything." },
                        { type: "comms", amount: 1, label: "Communication", color: 'purple' },
                        { type: "frontend", amount: 2, label: "Frontend dev", color: 'orange', info: "Must know React.js." },
                        { type: "media", amount: 2, label: "Media", color: 'red' },
                        { type: "backend", amount: 3, label: "Backend dev", color: 'blue' }
                    ],
                    students: [
                        { id: 1, name: "Friedrich Vandenberghe", role: "fullstack"},
                        { id: 2, name: "Lander Saerens", role: "frontend"},
                        { id: 3, name: "Simon Heemeryck", role: "backend"},
                        { id: 4, name: "Wouter Hennen", role: "frontend"},
                        { id: 5, name: "Lisa De Jonghe", role: "comms"},
                        { id: 6, name: "Henri Cattoire", role: "backend"},
                        { id: 7, name: "Lennart Veys", role: "backend"}
                    ]
                },
                {
                    id: 5,
                    title: "Project #3",
                    client: "Client #3",
                    coaches: [
                        { id: 1, name: "Miet" },
                        { id: 2, name: "Astrid" }
                    ],
                    roles: [
                        { type: "fullstack", amount: 2, label: "Full-Stack dev", color: 'green', info: "Must know everything." },
                        { type: "comms", amount: 1, label: "Communication", color: 'purple' },
                        { type: "frontend", amount: 2, label: "Frontend dev", color: 'orange', info: "Must know React.js." },
                        { type: "media", amount: 2, label: "Media", color: 'red' },
                        { type: "backend", amount: 3, label: "Backend dev", color: 'blue' }
                    ],
                    students: [
                        { id: 1, name: "Friedrich Vandenberghe", role: "fullstack"},
                        { id: 2, name: "Lander Saerens", role: "frontend"},
                        { id: 3, name: "Simon Heemeryck", role: "backend"},
                        { id: 4, name: "Wouter Hennen", role: "frontend"},
                        { id: 5, name: "Lisa De Jonghe", role: "comms"},
                        { id: 6, name: "Henri Cattoire", role: "backend"},
                        { id: 7, name: "Lennart Veys", role: "backend"}
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