<template>
  <div style="align-items: center; justify-content: center">
    <q-form
      class="createProjectForm q-py-lg"
      @submit="onSubmit"
    >
      <div>
        <div class="row justify-between items-center q-gutter-sm">
          <div class="text-bold text-h4 projectcol">
            Edit project "{{ projectStore.projectName }}"
          </div>
          <div>
            <div>
              <btn
                elevated
                color="warning"
                label="Cancel"
                type="cancel"
                size="md"
                class="q-mx-md cornered"
                glow-color="#00F1AF"
                shadow-strength="2"
                @click="cancelEditProject"
              />
              <btn
                elevated
                color="negative"
                label="Delete"
                type="delete"
                size="md"
                class="q-mx-md cornered"
                glow-color="#00F1AF"
                shadow-strength="2"
                @click="deleteProject"
              />
              <btn
                elevated
                color="positive"
                label="Update"
                type="submit"
                size="md"
                class="q-mx-md cornered"
                glow-color="#00F1AF"
                shadow-strength="2"
              />
            </div>
          </div>
        </div>
        <div class="row">
<!--          <p>-->
<!--            id: {{ id }}<br>-->
<!--            Name: {{ projectStore.projectName }}<br>-->
<!--            Partner name: {{ projectStore.projectPartnerName }}<br>-->
<!--            Link: {{ projectStore.projectLink }}<br>-->
<!--            Coachfilter: {{ projectStore.filterCoaches }}<br>-->
<!--            Coaches: {{ projectStore.selectedCoaches }}<br>-->
<!--            Skillstore skills: {{ skillStore.skills }}<br>-->
<!--          </p>-->

          <BasicInfo />

          <ProjectCoaches />

          <ProjectSkills />
        </div>
      </div>
    </q-form>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'
import { defineComponent, onMounted } from '@vue/runtime-core'
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'
import { useProjectStore } from '../../stores/useProjectStore'
import router from '../../router'
import BasicInfo from './components/BasicInfo.vue'
import ProjectCoaches from './components/ProjectCoaches.vue'
import ProjectSkills from './components/ProjectSkills.vue'
import { TempProjectSkill } from '../../models/Skill'

export default defineComponent({
  components: { ProjectCoaches, BasicInfo, ProjectSkills },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const projectID = ref(props.id)
    const skillStore = useSkillStore()
    const coachStore = useCoachStore()
    const projectStore = useProjectStore()

    onMounted(() => {
      coachStore.loadUsers()
      projectStore.getAndSetProject(
        projectID.value,
        (skills: TempProjectSkill[]) => {
          skillStore.setSkills(skills)
        }
      )
    })

    return {
      skillStore,
      coachStore,
      projectStore,
    }
  },
  methods: {
    onSubmit() {
      // TODO implement
      // this.projectStore.updateProject()
    },
    cancelEditProject() {
      router.push('/projects')
      this.projectStore.projectName = ''
      this.projectStore.projectPartnerName = ''
      this.projectStore.projectLink = ''
      this.projectStore.filterCoaches = ''
      this.projectStore.selectedCoaches = []
      this.skillStore.loadSkills()
    },
    deleteProject() {
      // TODO implement
    },
  },
})
</script>
<style>
thead {
  background-color: #44dba4;
}
</style>
<style scoped lang="sass">
.create-role-popup
  width: 300px

.cornered
  border-radius: 10px !important


.projectcol
  padding-left: 15px
  padding-right: 15px

.projectsubtitle
  margin-block-start: 0.5em !important
  font-weight: 300
  font-size: x-large

.table
  border-radius: 10px
  margin-top: 10px

.createProjectForm
  margin-left: 10%
  margin-right: 10%

.appPageTitle
  text-align: center
</style>
