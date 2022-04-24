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
            class="rounded-borders text-primary"
          >
            <q-item
              v-for="conflict in conflicts.entries()"
              :key="conflict[0]"
              v-ripple
              clickable
              :class="conflict[0].id === selectedStudent.id ? 'bg-teal-1' : ''"
              @click="selectedStudent = conflict[0]; studentProjects = conflict[1]"
            >
              <q-item-section>
                {{ fullName(conflict[0]) }}
              </q-item-section>
            </q-item>
          </q-list>
        </div>
        <div class="col">
          <div v-if="studentProjects.length !== 0">
            <masonry-wall
              ref="scrol"
              style="scroll-padding-top: 100px; overflow: auto; height: 92%"
              :items="studentProjects"
              :ssr-columns="1"
              :column-width="320"
              :gap="0"
              @scroll="showShadow = $event.target.scrollTop > 5"
            >
              <template #default="{ item }">
                <ProjectConflictCard :project="item" />
              </template>
            </masonry-wall>
          </div>
          <div v-else>
            Please select a student
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useProjectStore } from '../../stores/useProjectStore'
import ProjectConflictCard from "./components/ProjectConflictCard.vue"

export default defineComponent({
    components: { ProjectConflictCard },
    async setup() {
        const projectStore = useProjectStore()
        const conflicts = await projectStore.getConflictingProjects()
        const selectedStudent = ref({})
        const studentProjects = ref([])

        return {
            projectStore,
            conflicts,
            selectedStudent,
            showShadow: ref(false),
            studentProjects
        }
    },
    methods: {
      fullName(user: { firstName: string; lastName: string }) {
        return `${user.firstName} ${user.lastName}`
      }
    }
})
</script>

<style lang="sass">
.my-menu-link
  color: white
  background: #F2C037
</style>
