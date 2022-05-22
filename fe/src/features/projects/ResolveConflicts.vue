<template>
  <div style="height: 100%">
    <q-toolbar
      style="height: 8%; overflow: visible; z-index: 1"
      :class="`text-blue ${showShadow ? 'shadow-2' : ''}`"
    >
      <div
        class="text-bold text-h4 q-ml-md"
        :class="`text-${$q.dark.isActive ? 'white' : 'black'}`"
      >
        Conflicting Projects
      </div>
    </q-toolbar>
    <div
      class="q-pa-md"
    >
      <div class="row q-gutter-xl">
        <div class="col">
          <div v-if="selectedConflict.projects && selectedConflict.projects.length !== 0">
            <div
              id="scroll-target-id"
              style="flex:1; overflow: auto; "
            >
              <q-infinite-scroll
                :offset="250"
                scroll-target="#scroll-target-id"
                @load="onLoad"
              >
                <masonry-wall
                  ref="scrol"
                  style="scroll-padding-top: 100px; overflow: auto; height: 92%"
                  :items="selectedConflict.projects"
                  :ssr-columns="1"
                  :column-width="320"
                  :gap="0"
                >
                  <template #default="{ item }">
                    <div v-if="item">
                      <q-radio
                        v-model="selectedProjectId"
                        :val="(item as {id: number}).id"
                        label="Select this project"
                      />
                      <ProjectCard :project="item as any" expandable-skills />
                    </div>
                  </template>
                </masonry-wall>
                <template #loading>
                  <div class="row justify-center q-my-md">
                    <q-spinner
                      color="teal"
                      size="40px"
                    />
                  </div>
                </template>
              </q-infinite-scroll>
            </div>
          </div>
          <div v-else>
            Please select a student
          </div>
        </div>
        <div
          v-if="selectedConflict.projects && selectedConflict.projects.length !== 0"
          class="col-2"
        >
          <btn
            color="primary"
            label="Resolve"
            @click="resolveConflict()"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue'
import { Project } from '../../models/Project'
import { Student } from '../../models/Student'
import router from '../../router'
import { useProjectConflictStore } from '../../stores/useProjectConflictStore'
import ProjectCard from './components/ProjectCard.vue'
import MasonryWall from './MasonryWall.vue'

export default defineComponent({
    components: { ProjectCard, MasonryWall },
    setup() {
      const q = useQuasar()
      const projectConflictStore = useProjectConflictStore()

      return {
          q,
          selectedConflict: ref({student: {}} as { student: Student; projects: Project[] }),
          showShadow: ref(false),
          selectedProjectId: ref(-1),
          projectConflictStore
      }
    },
    watch: {
      'projectConflictStore.selectedStudentId': {
        handler(newValue) {
          this.selectStudent(newValue)
        }
      }
    },
    activated() {
      this.loadConflicts()
    },
    methods: {
      selectStudent(id: number) {
        this.selectedConflict = this.projectConflictStore.conflicts.find(c => c.student.id === id) as { student: Student; projects: Project[] }
      },
     selectedProject() {
        return this.selectedConflict.projects.filter(({id}) => id === this.selectedProjectId)[0]
     },
     async loadConflicts() {
       this.selectedConflict = {student: {}} as { student: Student; projects: Project[] }
       this.selectedProjectId = -1
       await this.projectConflictStore.getConflictingProjects()
     },
      async resolveConflict() {
        try {
          this.projectConflictStore.resolveConflict(this.selectedProject(), this.selectedConflict)
          await this.loadConflicts()

          if(this.projectConflictStore.conflicts.length == 0) router.push("/projects")
        } catch(error) {
          this.q.notify({
              icon: 'warning',
              color: 'red',
              message: `${error}`,
              textColor: 'black'
          });
        }
      },
      async onLoad(index: number, done: () => unknown) {
        if (this.projectConflictStore.nextPage !== null)
          await this.projectConflictStore.getConflictingProjects(this.projectConflictStore.nextPage)
        
        done()
      }
    }
})
</script>

<style lang="sass">
.my-menu-link
  color: white
  background: #F2C037
</style>
