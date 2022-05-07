<template>
  <div style="height: 100%">
    <SideBar
      :key="sideBarKey"
      :select-student="() => {}"
      :must-hover="true"
      color="bg-grey-3"
      draggable
    />
    <!-- <div > -->
    <div
      style="height: 100%"
      class="fit"
    >
      <q-toolbar
        style="height: 8%; overflow: visible; z-index: 1"
        :class="`text-blue bg-white ${showShadow ? 'shadow-2' : ''}`"
      >
        <div class="text-bold text-h4 q-ml-md text-black">
          Projects
        </div>
        <q-space />
        
          <!-- Do not remove the label attribute, otherwise the label slot does not work -->
          <q-input
            v-model="projectStore.projectFilter"
            debounce="300"
            dense
            outlined
            color="teal"
            label=""
            style="margin-top: 5px"
            class="text-bold"
            hide-bottom-space
          >
          <template v-slot:label>
            <span class="text-weight-medium text-teal-3">Search Projects</span>
          </template>
          <template v-slot:append>
            <q-icon name="search" color="teal-3" />
          </template>
          </q-input>
        <q-space />
        <btn
          padding="7px"
          :icon="expanded ? 'unfold_less' : 'unfold_more'"
          color="teal"
          shadow-color="teal"
          shadow-strength="1.8"
          @click="expanded = !expanded"
        />
        <btn
          padding="7px"
          icon="r_warning"
          color="red-7"
          to="/projects/conflicts"
          shadow-color="red"
          shadow-strength="2"
          no-wrap
        >
        <div class="ellipsis">Conflicts</div>
        </btn>
      </q-toolbar>

      <masonry-wall
        ref="scrol"
        style="overflow: auto; height: 92%"
        :items="projectStore.projects"
        :ssr-columns="1"
        :column-width="320"
        :gap="0"
        @scroll="showShadow = $event.target.scrollTop > 5"
      >
        <template #default="{ item }">
          <project-card :project="item" />
        </template>
      </masonry-wall>
    </div>

    <q-page-sticky
      position="bottom-right"
      :offset="[18, 18]"
    >
      <btn
        fab
        v-if="authenticationStore.loggedInUser?.isAdmin"
        padding="10px"
        icon="add"
        color="yellow"
        to="/projects/create"
        shadow-color="orange"
      />
    </q-page-sticky>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent } from 'vue'
import SideBar from '../../components/SideBar.vue'
import ProjectCard from './components/ProjectCard.vue'
import { useProjectStore } from '../../stores/useProjectStore'
import { useStudentStore } from "../../stores/useStudentStore";
import { useAuthenticationStore } from '../../stores/useAuthenticationStore'


export default defineComponent({
  name: 'ProjectList',
  components: { SideBar, ProjectCard },
  setup() {
  const baseURL =
    process.env.NODE_ENV == 'development'
      ? 'ws://localhost:8000/ws/socket_server/'
      : 'wss://sel2-5.ugent.be/ws/socket_server/'
    return {
      projectStore: useProjectStore(),
      studentStore: useStudentStore(),
      authenticationStore: useAuthenticationStore(),
      socket: new WebSocket(baseURL)
    }
  },
  data() {
    return {
      showShadow: ref(false),
      sideBarKey: 0,
    }
  },
  computed: {
    expanded: {
      get() {
        if (this.projectStore.projects.length === 0) return false
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return (this as any).projectStore.projects.every((p: { selectedRoles: any; }) => Object.values(p.selectedRoles ?? {k:false}).every(r => r))
      },
      set(newValue) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        this.projectStore.projects.forEach((p: any) => {
          for (let r in p.selectedRoles) {
            p.selectedRoles[r] = newValue
          }
        })
      }
    }
  },
  watch: {
    'projectStore.projectFilter': {
      handler() {
        this.projectStore.loadProjects()
      }
    }
  },
  created() {
    // Prevent a reload each time switched to the tab.
    if (this.projectStore.projects.length === 0)
      this.projectStore.loadProjects()
  },
  mounted() {
      this.socket.onmessage = async (event: { data: string }) => {
          const data = JSON.parse(event.data)

          if(data.hasOwnProperty('suggestion')) {
            await this.studentStore.receiveSuggestion(data.suggestion)
            this.sideBarKey += 1
          }
          else if(data.hasOwnProperty('remove_suggestion')) {
            this.studentStore.removeSuggestion(data.remove_suggestion)
            this.sideBarKey += 1
          }
          else if(data.hasOwnProperty('final_decision')) {
            this.studentStore.receiveFinalDecision(data.final_decision)
            this.sideBarKey += 1
          }
          else if(data.hasOwnProperty('remove_final_decision')) {
            this.studentStore.removeFinalDecision(data.remove_final_decision)
            this.sideBarKey += 1
          }
          else if(data.hasOwnProperty('suggest_student'))
            this.projectStore.receiveSuggestion(data.suggest_student)
          else if(data.hasOwnProperty('remove_student'))
            this.projectStore.removeReceivedSuggestion(data.remove_student)
      }
  }
})
</script>

<style>
.rotate180 {
  transform: rotate(180deg);
}
</style>

<style lang="sass" scoped>
.my-card
    border-radius: 10px !important

:deep(.q-btn--rectangle)
    border-radius: 12px !important

.q-btn
    margin: 5px
    
</style>
