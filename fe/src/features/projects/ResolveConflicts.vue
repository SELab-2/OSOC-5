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
              :key="conflict.student"
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
              @scroll="showShadow = $event.target.scrollTop > 5"
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
                      v-model="selectedProject"
                      :val="item"
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
import { useProjectConflictStore } from '../../stores/useProjectConflictStore'
import ProjectConflictCard from "./components/ProjectConflictCard.vue"

export default defineComponent({
    components: { ProjectConflictCard },
    async setup() {
        const $q = useQuasar()
        const projectConflictStore = useProjectConflictStore()
        await projectConflictStore.getConflictingProjects()

        return {
            q: $q,
            projectConflictStore,
            conflicts: projectConflictStore.conflicts,
            selectedConflict: ref({student: {}}),
            showShadow: ref(false),
            selectedProject: ref({})
        }
    },
    methods: {
      fullName(user: { firstName: string; lastName: string }) {
        return `${user.firstName} ${user.lastName}`
      },
      resolveConflict() {
        this.projectConflictStore.resolveConflict(this.selectedConflict as {
        student: Student
        projects: Array<Project>
      }, this.selectedProject as Project).catch((error) => {
        this.q.notify({
            icon: 'warning',
            color: 'red',
            message: `${error}`,
            textColor: 'black'
          });
      })
      },
      onLoad(index: never, done: () => unknown) {
        this.projectConflictStore.loadMoreProjects().then(() => done())
      }
    }
})
</script>

<style lang="sass">
.my-menu-link
  color: white
  background: #F2C037
</style>
