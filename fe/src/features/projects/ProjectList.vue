<template>
  <div
    style="overflow: hidden"
    class="fit column"
  >
    <div
      :class="`${showShadow ? 'shadow-2' : ''}`"
      style="z-index: 1; transition: box-shadow ease 500ms"
    >
      <q-toolbar
        style="overflow: visible; padding: 8px"
        :class="`bg-${$q.dark.isActive ? 'dark' : 'white'} text-${$q.dark.isActive ? 'white' : 'blue'}`"
      >
        <div class="text-bold text-h4 q-ml-md" :class="`text-${$q.dark.isActive ? 'white' : 'black'}`">Projects</div>
        <q-space />

        <btn
          round
          style="margin-top: 9px"
          size="12px"
          glow-color="teal-3"
          shadow-color="teal"
          :shadow-strength="showFilters ? 2 : 5"
          :color="showFilters ? 'teal' : 'transparent'"
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
          :color="expanded ? 'teal' : 'transparent'"
          :class="`text-${expanded ? 'white' : 'teal'}`"
          @click="expanded = !expanded"
        />

        <q-space />
        <btn
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
              <!-- <q-checkbox label="My project" /> -->
              <!-- <q-checkbox label="Students needed" /> -->
              
              <div style="min-width: 50%">
                <q-select
                  v-model="skillFilter"
                  clearable
                  rounded
                  outlined
                  dense
                  multiple
                  color="teal"
                  :options="skillStore.skills"
                  :option-label="opt => opt.name"
                  :dark="$q.dark.isActive"
                  label="Skills"
                  emit-value
                >
                  <template #selected>
                    <div
                      class="full-width"
                      style="max-height: 15vh; overflow-y: auto"
                    >
                      <StudentSkillChip
                        v-for="skill of skillFilter"
                        :key="(skill as {id: number}).id"
                        :color="(skill as {color: string}).color"
                        :name="(skill as {name: string}).name"
                        best-skill=""
                      />
                    </div>
                  </template>
                </q-select>
              </div>
              
              <div
                class="column q-mx-md"
              >
                <div class="col">
                  <q-checkbox 
                    v-model="onlyNotFull"
                    rounded
                    outlined
                    dense
                    color="teal"
                    bg-color="white"
                    label="Only show non-full projects"
                  />
                </div>
                <div class="col">
                  <q-checkbox 
                    v-model="onlyFull"
                    rounded
                    outlined
                    dense
                    color="teal"
                    bg-color="white"
                    label="Only show full projects"
                  />
                </div>
              </div>
            </div>
          </q-card-section>
        </div>
      </q-slide-transition>
    </div>

    <div
      id="scroll-target-id"
      ref="scroll"
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
          :scroll-target="$refs.scroll as any"
        >
          <template #default="{ item }">
            <project-card
              editable
              v-if="item"
              :project="item as any"
            />
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
import ProjectCard from './components/ProjectCard.vue'
import { useProjectStore } from '../../stores/useProjectStore'
import { useStudentStore } from '../../stores/useStudentStore'
import { useAuthenticationStore } from '../../stores/useAuthenticationStore'
import StudentSkillChip from "../students/components/StudentSkillChip.vue"
import { useSkillStore } from '../../stores/useSkillStore'
import { storeToRefs } from 'pinia'
import MasonryWall from './MasonryWall.vue'

export default defineComponent({
  name: 'ProjectList',
  components: { ProjectCard, MasonryWall, StudentSkillChip },
  setup() {
    const { loadNext } = useProjectStore()
    
    return {
      ...storeToRefs(useProjectStore()),
      loadNext,
      studentStore: useStudentStore(),
      authenticationStore: useAuthenticationStore(),
      skillStore: useSkillStore(),
    }
  },
  data() {
    return {
      showShadow: ref(false),
      showFilters: ref(false),
      projectNameFilter: ref(''),
      skillFilter: ref([]),
      onlyNotFull: false,
      onlyFull: false
    }
  },
  computed: {
    filters(): Object {
      const filters =  {
        search: this.projectNameFilter,
      } as { search: string; required_skills: never[]; full?: string }

      if(this.skillFilter && this.skillFilter.length)
        filters.required_skills = this.skillFilter.map(({id}) => id)
      else
        filters.required_skills = []

      if(this.onlyNotFull)
        filters.full = "false"
      else if(this.onlyFull)
        filters.full = "true"

      return filters
    },
    expanded: {
      get(): boolean {
        if (
          this.projects.length === 0 ||
          this.projects.some((p) => !p.requiredSkills)
        )
          return false
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return (this as any).projects
          .filter((p: any) => p.requiredSkills?.length > 0)
          .every((p: { selectedRoles: any }) =>
            Object.values(p.selectedRoles ?? { k: false }).every((r) => r)
          )
      },
      set(newValue: boolean) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        this.projects.forEach((p) => {
          for (let r in (p as any).selectedRoles) {
            (p as any).selectedRoles[r] = newValue
          }
        })
      },
    },
  },
  watch: {
    filters: {
      handler() {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const infscroll = this.$refs.infinite as any
        infscroll.reset()
        infscroll.resume()
        infscroll.trigger()
      },
    },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    onlyFull(newValue, _oldValue) {
      if(newValue == true) 
        this.onlyNotFull = false
    },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    onlyNotFull(newValue, _oldValue) {
      if(newValue == true) 
        this.onlyFull = false
    }
  },
  activated() {
    // Check if the projects list has been altered in another view.
    // If this flag is set, the view resets the pagination and loads all the projects.
    if (this.shouldRefresh) {
      this.shouldRefresh = false
      const infscroll = this.$refs.infinite as any
      infscroll.reset()
      infscroll.resume()
      infscroll.trigger()
    }
  },
})
</script>

<style>
.rotate180 {
  transform: rotate(180deg);
}
</style>

<style lang="sass" scoped>

:deep(.q-btn--rectangle)
    border-radius: 12px !important

.q-btn
    margin: 5px
</style>
