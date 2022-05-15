<template>
  <div
    style="overflow: hidden"
    class="fit column"
  >
    <div
      :class="`${showShadow ? 'shadow-2' : ''}`"
      style="z-index: 1; transition: box-shadow ease 500ms;"
    >
      <q-toolbar
        style="overflow: visible; padding: 8px"
        class="text-blue bg-white"
      >
        <div class="text-bold text-h4 q-ml-md text-black">
          Projects
        </div>
        <q-space />

        <btn
          round
          style="margin-top: 9px"
          size="12px"
          glow-color="teal-3"
          shadow-color="teal"
          :shadow-strength="showFilters ? 2 : 5"
          :color="showFilters ? 'teal' : 'white'"
          :class="`text-${showFilters ? 'white' : 'teal'}`"
          icon="tune"
          @click="showFilters = !showFilters"
        />
        <!-- Do not remove the label attribute, otherwise the label slot does not work -->
        <q-input
          v-model="projectNameFilter"
          tabindex="-1"
          debounce="300"
          dense
          outlined
          color="teal"
          label=""
          style="margin-top: 5px"
          hide-bottom-space
        >
          <template #label>
            <span class="text-weight-medium text-teal-3">Search Projects</span>
          </template>
          <template #append>
            <q-icon
              name="search"
              color="teal-3"
            />
          </template>
        </q-input>
        <btn
          round
          style="margin-top: 9px"
          size="12px"
          :icon="expanded ? 'unfold_less' : 'unfold_more'"
          glow-color="teal-3"
          shadow-color="teal"
          :shadow-strength="expanded ? 2 : 5"
          :color="expanded ? 'teal' : 'white'"
          :class="`text-${expanded ? 'white' : 'teal'}`"
          @click="expanded = !expanded"
        />

        <q-space />
        <btn
          v-if="conflictsExists"
          padding="7px"
          icon="r_warning"
          color="red-7"
          to="/projects/conflicts"
          shadow-color="red"
          shadow-strength="2"
          no-wrap
        >
          <div class="ellipsis">
            Conflicts
          </div>
        </btn>
      </q-toolbar>

      <q-slide-transition style="height: fit-content">
        <div v-if="showFilters">
          <q-card-section>
            <span class="text-h5 text-bold">Filters</span><br>
            <div class="row">
              <div class="column">
                <!-- <q-checkbox label="My project" /> -->
                <!-- <q-checkbox label="Students needed" /> -->
              </div>
              <!-- <div>
                <q-select
                  v-model="studentStore.skills"
                  rounded
                  outlined
                  dense
                  multiple
                  color="primary"
                  bg-color="white"
                  :options="skillStore.skills"
                  :option-label="(opt) => opt.name"
                  :option-value="(opt) => opt.id"
                  label="Skills"
                  style="width: 200px"
                >
                  <template #selected>
                    <div
                      class="full-width"
                      style="max-height: 15vh; overflow-y: auto"
                    >
                      <StudentSkillChip
                        v-for="skill of studentStore.skills"
                        :key="skill.id"
                        :color="skill.color"
                        :name="skill.name"
                        best-skill=""
                      />
                    </div>
                  </template>
                </q-select>
              </div> -->
            </div>
          </q-card-section>
        </div>
      </q-slide-transition>
    </div>

    <div
      id="scroll-target-id"
      style="flex: 1; overflow: auto"
      @scroll="showShadow = ($event.target as HTMLElement)?.scrollTop > 5"
    >
      <q-infinite-scroll
        ref="infinite"
        :offset="250"
        scroll-target="#scroll-target-id"
        @load="(i, done) => loadNext(i, done, filters)"
      >
        <masonry-wall
          :items="projects"
          :ssr-columns="1"
          :column-width="320"
          :gap="0"
        >
          <template #default="{ item }">
            <project-card :project="item" />
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

  <q-page-sticky
    position="bottom-right"
    :offset="[18, 18]"
  >
    <btn
      v-if="authenticationStore.loggedInUser?.isAdmin"
      fab
      padding="10px"
      icon="add"
      color="yellow"
      to="/projects/create"
      shadow-color="orange"
    />
  </q-page-sticky>
</template>

<script lang="ts">
import { ref, defineComponent } from 'vue'
import SideBar from '../../components/SideBar.vue'
import ProjectCard from './components/ProjectCard.vue'
import { useProjectStore } from '../../stores/useProjectStore'
import { useStudentStore } from '../../stores/useStudentStore'
import { useAuthenticationStore } from '../../stores/useAuthenticationStore'
import { useSkillStore } from '../../stores/useSkillStore'
import { storeToRefs } from 'pinia'
import { instance } from '../../utils/axios'

export default defineComponent({
  name: 'ProjectList',
  components: { SideBar, ProjectCard },
  setup() {
    const baseURL =
      process.env.NODE_ENV == 'development'
        ? 'ws://localhost:8000/ws/socket_server/'
        : 'wss://sel2-5.ugent.be/ws/socket_server/'
        
    const { loadNext, receiveSuggestion, removeReceivedSuggestion} = useProjectStore()
    return {
      ...storeToRefs(useProjectStore()),
      loadNext,
      receiveSuggestion,
      removeReceivedSuggestion,
      studentStore: useStudentStore(),
      authenticationStore: useAuthenticationStore(),
      skillStore: useSkillStore(),
      socket: new WebSocket(baseURL),
    }
  },
  data() {
    return {
      showShadow: ref(false),
      showFilters: ref(false),
      projectNameFilter: ref(''),
      conflictsExists: ref(true),
    }
  },
  computed: {
    filters(): Object {
      return {
        search: this.projectNameFilter,
      }
    },
    expanded: {
      get() {
        if (this.projects.length === 0) return false
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return (this as any).projects.every(
          (p: { selectedRoles: any }) =>
            Object.values(p.selectedRoles ?? { k: false }).every((r) => r)
        )
      },
      set(newValue) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        this.projects.forEach((p: any) => {
          for (let r in p.selectedRoles) {
            p.selectedRoles[r] = newValue
          }
        })
      },
    },
  },
  watch: {
    projectNameFilter: {
      handler() {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const infscroll = this.$refs.infinite as any;
        infscroll.reset()
        infscroll.resume()
        infscroll.trigger()
      },
    },
  },
  mounted() {
    this.socket.onmessage = async (event: { data: string }) => {
      const data = JSON.parse(event.data)

      if (data.hasOwnProperty('suggestion')) {
        await this.studentStore.receiveSuggestion(data.suggestion)
      } else if (data.hasOwnProperty('remove_suggestion')) {
        this.studentStore.removeSuggestion(data.remove_suggestion)
      } else if (data.hasOwnProperty('final_decision')) {
        this.studentStore.receiveFinalDecision(data.final_decision)
      } else if (data.hasOwnProperty('remove_final_decision')) {
        this.studentStore.removeFinalDecision(data.remove_final_decision)
      } else if (data.hasOwnProperty('suggest_student'))
        this.receiveSuggestion(data.suggest_student)
      else if (data.hasOwnProperty('remove_student'))
        this.removeReceivedSuggestion(data.remove_student)
    }

    instance.get('projects/get_conflicting_projects').then(({data}) => {
      this.conflictsExists = data.count > 0
    })
  },  
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
