<template>
  <div style="height: 100%">
    <q-toolbar
      style="height: 8%; overflow: visible; z-index: 1"
      :class="`text-blue bg-white ${showShadow ? 'shadow-2' : ''}`"
    >
      <div class="text-bold text-h4 q-ml-md text-black">
        Conflicting projects
      </div>
    </q-toolbar>
    <div
      class="q-pa-md"
    >
      <div class="row q-gutter-xl">
        <div
          class="col-2"
          style="max-width: 250px"
        >
          <q-list
            bordered
            padding
            separator
            class="rounded-borders"
          >
            <q-item
              v-for="conflict in conflicts"
              :key="conflict.student.url"
              v-ripple
              clickable
              :class="conflict.student.id === selectedConflict.student.id ? 'bg-teal-1' : ''"
              @click="selectedConflict = conflict"
            >
              <q-item-section>
                {{ fullName(conflict.student) }}
              </q-item-section>
            </q-item>
          </q-list>
        </div>
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
                  @scroll="showShadow = $event.target.scrollTop > 5"
                >
                  <template #default="{ item }">
                    <q-radio
                      v-model="selectedProjectId"
                      :val="item.id"
                      label="Select this project "
                    />
                    <ProjectConflictCard :project="item" />
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
          <q-btn
            color="primary"
            label="Submit"
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
import { useProjectStore } from '../../stores/useProjectStore'
import { useStudentStore } from '../../stores/useStudentStore'
import { instance } from '../../utils/axios'
import ProjectConflictCard from "./components/ProjectConflictCard.vue"

export default defineComponent({
    components: { ProjectConflictCard },
    async setup() {
      const $q = useQuasar()

      return {
          q: $q,
          selectedConflict: ref({student: {}} as { student: Student; projects: Project[] }),
          showShadow: ref(false),
          selectedProjectId: ref(-1),
          conflicts: ref([] as { student: Student; projects: Project[]; }[]),
          nextPage: ref("")
      }
    },
    async mounted() {
     await this.loadConflicts()
    },
    methods: {
     selectedProject() {
        return this.selectedConflict.projects.filter(({id}) => id === this.selectedProjectId)[0]
     },
     async loadConflicts() {
       this.selectedConflict = {student: {}} as { student: Student; projects: Project[] }
       this.selectedProjectId = -1
       const projects = await this.getConflictingProjects()
       this.conflicts = projects.conflicts
       this.nextPage = projects.nextPage
     },
     async getConflictingProjects(url?: string) {
      const studentStore = useStudentStore()
      const projectStore = useProjectStore()

      const { data } = await instance.get(
        url ?? 'projects/get_conflicting_projects'
      )

      const conflicts = data.results as Array<{
        student: string
        projects: Array<string>
      }>

      const resConflicts = []
      for (const conflict of conflicts) {
        const student = await studentStore.getStudent(conflict.student)
        const projects = await Promise.all(
          conflict.projects.map(
            async (project: string) =>
              await projectStore.getOrFetchProject(project)
          )
        )

        resConflicts.push({ student, projects })
      }

      return {conflicts: resConflicts, nextPage: data.next}
      },
      fullName(user: { firstName: string; lastName: string }) {
        return `${user.firstName} ${user.lastName}`
      },
      async resolveConflict() {
        try {
          const suggestions = this.selectedProject().suggestedStudents?.filter(
            ({ student }) => student.id === this.selectedConflict.student.id
           )

          if (!suggestions) throw new Error('An unexpected error has occured')

          if (suggestions?.length > 1)
            throw new Error(
              'Please delete the assignment to skills until only 1 is left'
            )

          const suggestion = suggestions[0]

          await instance.post('/projects/resolve_conflicts/', [
            {
              project: this.selectedProject().url,
              student: this.selectedConflict.student.url,
              coach: suggestion.coach.url,
              skill: suggestion.skill.url,
          },
        ])

        const projectStore = useProjectStore()
        await projectStore.loadProjects() 
        await this.loadConflicts()
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
        if (this.nextPage !== null)
          await this.getConflictingProjects(this.nextPage)
        
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
