<template>
  <div style="align-items: center; justify-content: center">
    <q-form class="createProjectForm q-py-lg" @submit="onSubmit">
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
                @click="updateProject"
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

      <q-dialog
        class="full-width"
        :model-value="deleteProjectID !== -1"
        persistent
        @update:model-value="deleteProjectID = -1"
      >
        <DeleteProjectDialog
          :delete-project-id="deleteProjectID"
          :delete-project-name="deleteProjectName"
        />
      </q-dialog>
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
import DeleteProjectDialog from './components/subcomponents/DeleteProjectDialog.vue'

export default defineComponent({
  components: { ProjectCoaches, BasicInfo, ProjectSkills, DeleteProjectDialog },
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

    const deleteProjectID = ref(-1)
    const deleteProjectName = ref('')

    onMounted(() => {
      coachStore.loadUsers()
      projectStore
        .getAndSetProject(projectID.value, (skills: TempProjectSkill[]) => {
          skillStore.setSkills(skills)
        })
        // this happens when user requests invalid project id
        .catch(() => router.push('/projects'))
    })

    return {
      projectID,
      skillStore,
      coachStore,
      projectStore,
      deleteProjectID,
      deleteProjectName,
    }
  },
  methods: {
    updateProject() {
      console.log('updateProject') //TODO REMOVE
      // TODO implement
      // CHECK IF ALLE VELDEN GOED ZIJN of stuur patch die enkel velden update die goed zin
      // this.projectStore.updateProject()
      this.$q.notify({
        icon: 'close',
        color: 'negative',
        message: 'Not yet implemented!',
      })
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
      this.deleteProjectID = +this.projectID
      this.deleteProjectName = this.projectStore.projectName
    },
    onSubmit() {
      // do nothing, but we need to catch this since otherwise the url changes
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
