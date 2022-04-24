<template>
  <div style="height: 100%">
    <SideBar
      :select-student="() => {}"
      :must-hover="true"
      color="bg-grey-3"
      draggable
    />
    <!-- <div > -->
    <div style="height: 100%" class="fit">
      <q-toolbar
        style="height: 8%; overflow: visible; z-index: 1"
        :class="`text-blue bg-white ${showShadow ? 'shadow-2' : ''}`"
      >
        <div class="text-bold text-h4 q-ml-md text-black">Projects</div>
        <q-space />
        <div>
          <q-input dense v-model="filter" outlined label="Outlined" style="margin-right: 10px" />
        </div>
        <btn
          padding="7px"
          :icon="expanded ? 'unfold_less' : 'unfold_more'"
          color="blue"
          @click="expanded = !expanded"
          shadow-color="blue"
          shadow-strength="1.8"
        />
        <btn
          padding="7px"
          icon="r_warning"
          color="red"
          label="Conflicts"
          to="/projects/conflicts"
          shadow-color="red"
          shadow-strength="2.5"
        />
      </q-toolbar>

      <masonry-wall
        ref="scrol"
        @scroll="showShadow = $event.target.scrollTop > 5"
        style="scroll-padding-top: 100px; overflow: auto; height: 92%"
        :items="projectStore.projects"
        :ssr-columns="1"
        :column-width="320"
        :gap="0"
      >
        <template #default="{ item }">
          <project-card :project="item" />
        </template>
      </masonry-wall>
    </div>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <btn
        fab
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

export default defineComponent({
  name: 'ProjectList',
  components: { SideBar, ProjectCard },
  data() {
    return {
      filter: ref(''),
      showShadow: ref(false),
    }
  },
  setup() {
    const projectStore = useProjectStore()
    return {
      projectStore,
    }
  },
  created() {
    // Prevent a reload each time switched to the tab.
    if (this.projectStore.projects.length === 0)
      this.projectStore.loadProjects()
  },
  computed: {
    expanded: {
      get() {
        if (this.projectStore.projects.length === 0) return false
        return (this as any).projectStore.projects.every((p: any) => Object.values(p.selectedRoles ?? {k:false}).every(r => r))
      },
      set(newValue) {
        this.projectStore.projects.forEach((p: any) => {
          for (let r in p.selectedRoles) {
            p.selectedRoles[r] = newValue
          }
        })
      }
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
