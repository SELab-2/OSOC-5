<template>
  <q-splitter
    v-model="_splitterModel"
    :limits="step === 0 ? [50, 50] : showPreview ? [40, 80] : [100, 100]"
    emit-immediately
    style="height: 100%; overflow: hidden"
    :before-class="disabled ? '' : 'resize-container'"
    @update:modelValue="showPreview ? disable() : ''"
  >
    <q-resize-observer @resize="onResize" />

    <template #before>
      <q-stepper
        v-if="project"
        v-model="step"
        class="column"
        style="height: 100%"
        active-icon="none"
        error-icon="none"
        done-color="teal"
        active-color="teal"
        error-color="teal"
        animated
        keep-alive
        header-nav
        flat
      >
        <q-step
          :name="0"
          title="Project Info"
          icon="r_info"
          :done="basicInfoDone"
          :caption="
            visitedSteps[0] && !basicInfoDone
              ? 'Empty Fields Left'
              : project?.name
          "
        >
          <BasicInfo
            v-model:name="project.name"
            v-model:partnerName="project.partnerName"
            v-model:info="project.extraInfo"
          />
        </q-step>

        <q-step
          :name="1"
          title="Coaches"
          icon="r_group"
          :done="visitedSteps[1]"
          :caption="`${project?.coaches?.length} Coach${
            project?.coaches?.length !== 1 ? 'es' : ''
          } Selected`"
        >
          <ProjectCoaches :coaches="project!.coaches!" />
        </q-step>

        <q-step
          :name="2"
          title="Skills"
          icon="r_build"
          :done="visitedSteps[2]"
          :caption="`${project?.requiredSkills?.length} Skill${
            project?.requiredSkills?.length !== 1 ? 's' : ''
          } Selected`"
        >
          <ProjectSkills :skills="project!.requiredSkills!" />
        </q-step>
      </q-stepper>
      <btn
        v-if="step > 0"
        style="position: absolute; left: 0; bottom: 0"
        class="q-ma-md"
        padding="10px"
        icon="arrow_back"
        label="Previous"
        color="teal"
        shadow-color="teal"
        @click="step -= 1"
      />
      <btn
        v-if="step < 2 && (showPreview || id === undefined)"
        style="position: absolute; right: 0; bottom: 0"
        padding="10px"
        class="q-ma-md"
        icon-right="arrow_forward"
        label="Next"
        color="teal"
        shadow-color="teal"
        @click="next"
      />
    </template>
    <template #after>
      <div
        v-if="project && showPreview"
        class="column fit justify-center items-center content-center"
      >
        <div class="text-h6 text-bold">
          Preview
        </div>
        <project-card
          v-model:expandedInfo="showInfo"
          style="width: 90%; max-width: 400px"
          :project="project"
        />
        <q-slide-transition>
          <div
            v-if="showDelete"
            style="width: 70%; text-align: center;"
          >
            <div class="q-gutter-sm q-mb-md">
              <div class="text-subtitle2 text-bold text-red">
                Are you sure you want to delete this project?<br>This action cannot be undone.
              </div>
              <div>Please type the name of the project to confirm:</div>
              <div class="row justify-center q-gutter-sm">
                <q-input
                  v-model="deleteConfirmation"
                  type="text"
                  outlined
                  color="red"
                  dense
                  :placeholder="project!.name"
                />
                <btn
                  label="confirm"
                  dense
                  color="red"
                  shadow-color="red"
                  :disabled="deleteConfirmation !== project.name"
                  shadow-strength="2"
                  @click="deleteProject"
                />
              </div>
            </div>
          </div>
        </q-slide-transition>
      </div>
    </template>
  </q-splitter>
  <div
    style="position: absolute; right: 0; bottom: 0"
    class="q-gutter-md q-ma-md"
  >
    <btn
      v-if="id"
      padding="10px"
      icon="delete"
      label="Delete"
      glow-color="red"
      glow-size="1500px"
      color="teal"
      shadow-color="teal"
      @click="showDelete = !showDelete; deleteConfirmation = ''; showInfo = true"
    />
    <btn
      v-if="basicInfoDone"
      padding="10px"
      :icon-right="!showPreview && step < 2 ? 'arrow_forward' : 'check'"
      :label="!showPreview && step < 2 ? 'Next' : id !== undefined ? 'Update' : 'Publish'"
      color="teal"
      shadow-color="teal"
      @click="showPreview ? submit() : next()"
    />
  </div>
</template>

<script lang="ts">
import { ref, Ref, defineComponent } from 'vue'
import BasicInfo from './components/BasicInfo.vue'
import ProjectCoaches from './components/ProjectCoaches.vue'
import ProjectSkills from './components/ProjectSkills.vue'
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'
import { useProjectStore } from '../../stores/useProjectStore'
import { useAuthenticationStore } from '../../stores/useAuthenticationStore'
import { Project } from '../../models/Project'
import router from '../../router'
import ProjectCard from './components/ProjectCard.vue'

export default defineComponent({
  name: 'CreateProject',
  components: { BasicInfo, ProjectCoaches, ProjectSkills, ProjectCard },
  props: {
    id: {
      type: Number,
      required: false,
    },
  },
  data() {
    let timeout: any | null = null

    const projectStore = useProjectStore()
    const project: Ref<Project | null> = ref(null)
    return {
      step: ref(0),
      visitedSteps: ref([false, false, false, false]),
      skillStore: useSkillStore(),
      coachStore: useCoachStore(),
      projectStore: useProjectStore(),
      project,
      splitterModel: ref(70),
      width: ref(0),
      disabled: ref(false),
      timeout,
      showDelete: ref(false),
      deleteConfirmation: ref('')
    }
  },
  computed: {
    basicInfoDone(): boolean {
      if (!this.project) return false
      return this.project.name.length > 0 && this.project.partnerName.length > 0
    },
    showInfo: {
      get(): boolean {
        return this.step === 0 || this.showDelete
      },
      set(n: boolean) {
        this.step = 0
      },
    },
    showPreview() {
      return this.width > 1200 || this.step === 0
    },
    _splitterModel: {
      get(): number {
        return this.showPreview
          ? this.step === 0
            ? 50
            : this.splitterModel
          : 100
      },
      set(n: number) {
        if (n > 80) return
        this.splitterModel = n
      },
    },
  },
  watch: {
    step(newValue, oldValue) {
      this.visitedSteps[oldValue] = true
    },
  },
  async mounted() {
    if (!useAuthenticationStore().loggedInUser?.isAdmin) {
      router.replace('/notfound')
      return
    }
    let project: Project
    if (this.id) {
      try {
        project = await this.projectStore.getProject(this.id)
      } catch (error) {
        router.replace('/notfound')
        return
      }
    } else {
      project = new Project('', '', '', 0, "", [], [])
    }
    this.project = project
  },
  methods: {
    next() {
      if (this.step < 2) {
        this.step += 1
      } else {
        this.submit()
      }
    },
    async submit() {
      if (this.id) {
        let error = await this.projectStore.updateProject(this.project!, this.project!.id)
        this.displayErrorOr(error, () => {
          this.projectStore.shouldRefresh = true
          router.push('/projects')
        })
      } else {
        let error = await this.projectStore.addProject(this.project!)
        this.displayErrorOr(error, () => {
          this.projectStore.shouldRefresh = true
          router.replace('/projects')
        })
      }
    },
    async deleteProject() {
      let error = await this.projectStore.deleteProject(this.project!.id)
      this.displayErrorOr(error, () => {
        this.projectStore.shouldRefresh = true
        router.replace('/projects')
      })
    },
    displayErrorOr(error: any, other: Function) {
      if (error) {
        this.$q.notify({
          icon: 'error',
          color: 'warning',
          message: error.detail,
        })
      } else {
        other()
      }
    },
    onResize(e: { width: number }) {
      this.width = e.width
    },
    disable() {
      console.log('Hello')
      this.disabled = true
      clearTimeout(this.timeout)
      this.timeout = setTimeout(() => {
        this.disabled = false
      }, 200)
    },
  },
})
</script>

<style lang="sass">
.resize-container
  transition: all .3s
</style>

<style scoped>
:deep(.q-stepper__content) {
  flex: 1;
}

:deep(.q-stepper__step-content),
:deep(.q-stepper__step-inner) {
  height: 100%;
}

</style>
