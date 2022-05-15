<template>
  <div style="align-items: center; justify-content: center">
    <q-form class="createProjectForm q-py-lg" @submit="onSubmit">
      <div>
        <div class="row justify-center justify-between items-center q-gutter-sm">
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
                shadow-strength="2"
                :to="`/projects`"
              />
              <btn
                elevated
                color="negative"
                label="Delete"
                type="delete"
                size="md"
                class="q-mx-md cornered"
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
                shadow-strength="2"
                @click="updateProject"
              />
            </div>
          </div>
        </div>
        <div class="row">
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
  name: 'EditProject',
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
    // this function updates a project given the ID and the current selected skills
    updateProject() {
      this.projectStore.updateProject(this.projectID, this.skillStore.skills, (positive: boolean) => {
        // if the call is a success, we give a positive notification
        if (positive) {
          router.push('/projects')
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Successfully updated project!',
          })
        } else { // otherwise we tell the user it failed
          this.$q.notify({
            icon: 'close',
            color: 'negative',
            message: 'Failed to update project!',
          })
        }
      })
    },
    // to delete a project, we set the id, and the DeleteDialog will open
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
  margin-left: 5%
  margin-right: 5%

.appPageTitle
  text-align: center
</style>
