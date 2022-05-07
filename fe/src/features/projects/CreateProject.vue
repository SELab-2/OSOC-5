<template>
  <div style="align-items: center; justify-content: center">
    <q-form
      class="createProjectForm q-py-lg"
      @submit="onSubmit"
    >
      <div>
        <div class="row justify-between items-center q-gutter-sm">
          <div class="text-bold text-h4 projectcol">
            Create project
          </div>
          <div>
            <div>
              <btn
                elevated
                color="primary"
                label="Cancel"
                type="cancel"
                size="md"
                class="q-mx-md cornered"
                glow-color="#00F1AF"
                shadow-strength=2
                @click="onCancel"
              />
              <btn
                elevated
                color="primary"
                label="Submit"
                type="submit"
                size="md"
                class="q-mx-md cornered"
                glow-color="#00F1AF"
                shadow-strength=2
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
    </q-form>
  </div>
</template>

<script lang="ts">
import router from '../../router'
import { defineComponent, onMounted } from '@vue/runtime-core'
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'
import BasicInfo from "./components/BasicInfo.vue";
import {useProjectStore} from "../../stores/useProjectStore";
import ProjectCoaches from "./components/ProjectCoaches.vue";
import {useAuthenticationStore} from "../../stores/useAuthenticationStore";
import ProjectSkills from "./components/ProjectSkills.vue";

export default defineComponent({
  components: {ProjectCoaches, BasicInfo, ProjectSkills},
  setup() {
    const skillStore = useSkillStore()
    const coachStore = useCoachStore()
    const projectStore = useProjectStore()



    return {
      skillStore,
      coachStore,
      projectStore,
      authenticationStore: useAuthenticationStore(),

    }
  },
  beforeMount() {
  if (!this.authenticationStore.loggedInUser?.isAdmin) {
    router.replace('/projects')
  }
  },
  mounted(){
    this.skillStore.loadSkills()
    this.coachStore.loadUsers()
  // makes sure the fields are empty
    this.projectStore.projectName = ''
    this.projectStore.projectPartnerName = ''
    this.projectStore.projectLink = ''
    this.projectStore.filterCoaches = ''
    this.projectStore.selectedCoaches = []
  },
  methods: {
    onSubmit() {
      this.projectStore.submitProject(
        this.skillStore.skills,
        (success: boolean) => {
          if (success) {
            router.push('/projects')

            this.$q.notify({
              icon: 'done',
              color: 'positive',
              message: 'Project created successfully!',
            })
          } else {
            this.$q.notify({
              icon: 'close',
              color: 'negative',
              message: 'Project creation failed',
            })
          }
        }
      )
    },
    onCancel(){
      router.push('/projects')
      this.projectStore.projectName= ''
      this.projectStore.projectPartnerName= ''
      this.projectStore.projectLink= ''
      this.projectStore.filterCoaches=''
      this.projectStore.selectedCoaches= []
      this.skillStore.loadSkills()
    }
  }
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
