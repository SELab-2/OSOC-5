<template>
  <div>
    <q-drawer
      v-model="showDrawer"
      :mini="miniState"
      :mini-width="30"
      :width="370"
      :breakpoint="100"
      class="bg-grey-1 shadow-4"
    >
      <div
        :style="!miniState? '' : 'display: none'"
        style="height: 100%; overflow: hidden;"
        class="fit column"
      >
        <div
          :class="`${showShadow ? 'shadow-2' : ''}`"
          style="z-index: 1; transition: box-shadow ease 500ms"
          class="q-px-sm"
        >
          <div class="text-bold text-h5 q-py-sm">
            Students
          </div>
          <div class="row no-wrap q-pb-sm">
            <q-input
              v-model="search"
              debounce="300"
              class="fit q-mr-sm"
              dense
              outlined
              color="teal"
              label="Search Students"
              hide-bottom-space
              @update:modelValue="async () => await loadStudents($refs.infiniteScroll)"
            >
              <template #append>
                <q-icon
                  name="search"
                  color="teal-4"
                />
              </template>
            </q-input>
            <btn
              round
              size="0.95em"
              glow-color="teal-2"
              shadow-color="osoc-red"
              :shadow-strength="showFilters ? 2 : 5"
              :color="showFilters ? 'primary' : 'light-grey'"
              :class="`text-${showFilters ? 'white' : 'green'}`"
              icon="tune"
              @click="showFilters = !showFilters"
            />
          </div>
          <q-slide-transition>
            <div
              v-if="showFilters"
              class="overflow-hidden"
            >
              <!-- div needs to be wrapped because gutter produces negative margins, which cause issues with q-slide-transition -->
              <div class="q-gutter-y-sm q-px-xs">
                <SegmentedControl
                  v-model="alumni"
                  color="primary"
                  text-color="white"
                  class="q-mt-md"
                  :options="[
                    { name: 'all', label: 'All' },
                    { name: 'alumni', label: 'Alumni' },
                    { name: 'student coaches', label: 'Student Coaches'}
                  ]"
                  @click="async () => await loadStudents($refs.infiniteScroll)"
                />

                <label>Suggestion:</label>
                <SegmentedControl
                  v-model="suggestion"
                  color="primary"
                  :options="[
                    { name: 'yes', label: 'Yes' },
                    { name: 'maybe', label: 'Maybe' },
                    { name: 'no', label: 'No' },
                    { name: 'none', label: 'None' },
                  ]"
                  @click="async () => await loadStudents($refs.infiniteScroll)"
                />

                <q-select
                  v-model="skills"
                  clearable
                  rounded
                  outlined
                  dense
                  multiple
                  color="primary"
                  bg-color="white"
                  :options="skillStore.skills"
                  :option-label="opt => opt.name"
                  :option-value="opt => opt.id"
                  label="Skills"
                  @update:model-value="async () => await loadStudents($refs.infiniteScroll)"
                >
                  <template #selected>
                    <div
                      class="full-width"
                      style="max-height: 15vh; overflow-y: auto"
                    >
                      <StudentSkillChip
                        v-for="skill of skills"
                        :key="(skill as any).id"
                        :color="(skill as any).color"
                        :name="(skill as any).name"
                        best-skill=""
                      />
                    </div>
                  </template>
                </q-select>

                <q-select
                  v-model="status"
                  rounded
                  outlined
                  dense
                  clearable
                  color="primary"
                  bg-color="white"
                  :options="stati"
                  :option-label="opt => opt.label"
                  :option-value="opt => opt.value"
                  label="Status"
                  emit-value
                  map-options
                  @update:model-value="async () => await loadStudents($refs.infiniteScroll)"
                />

                <div class="row q-gutter-x-md">
                  <q-checkbox
                    v-model="byMe"
                    toggle-indeterminate
                    false-value="maybe"
                    indeterminate-value="false"
                    toggle-order="tf"
                    color="primary"
                    label="Suggested by you"
                    right-label
                    @click="async () => await loadStudents($refs.infiniteScroll)"
                  />
                  <q-checkbox
                    v-model="onProject"
                    toggle-indeterminate
                    true-value="true"
                    false-value="maybe"
                    indeterminate-value="false"
                    toggle-order="tf"
                    color="primary"
                    label="On project"
                    right-label
                    @click="async () => await loadStudents($refs.infiniteScroll)"
                  />
                </div>
              </div>
            </div>
          </q-slide-transition>
        </div>

        <q-scroll-area
          class="fadeOut q-px-sm"
          :thumb-style="thumbStyle"
          style="flex: 1; overflow: hidden;"
          @scroll="showShadow = $event.verticalPosition > 5"
        >
          <q-infinite-scroll
            ref="infiniteScroll"
            class="q-pa-sm"

            :offset="250"
            @load="async (index, done) => await studentStore.loadNext(index, done, filters)"
          >
            <StudentCard
              v-for="student in studentStore.students"
              :id="student.email"
              :key="student.email"

              class="q-ma-sm"
              :draggable="onProjectsPage"
              :must-hover="onProjectsPage"
              :student="student"
              :active="studentStore.currentStudent ? student.email === studentStore.currentStudent.email : false"
              @click="$router.push(`/students/${student.id}`)"
              @dragstart="onDragStart($event, student)"
            />
            <template #loading>
              <div class="row justify-center q-my-md">
                <q-spinner-dots
                  color="primary"
                  size="40px"
                />
              </div>
            </template>
          </q-infinite-scroll>
        </q-scroll-area>
      </div>

      <!--      <q-inner-loading-->
      <!--        :showing="studentStore.isLoading"-->
      <!--        label="Please wait..."-->
      <!--        label-class="text-teal"-->
      <!--        label-style="font-size: 1.1em"-->
      <!--      />-->

      <div
        class="absolute"
        style="top: 15px; right: -17px; z-index: 2;"
      >
        <btn
          dense
          shadow-color="yellow"
          shadow-strength="1"
          color="yellow"
          :icon="!miniState? 'chevron_left' : 'chevron_right'"
          :style="`transform: translate(${showDrawer ? 0 : -50}%)`"
          style="transition: translate ease 500ms;"
          @click="miniState = !miniState"
        />
      </div>
    </q-drawer>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue'
import SegmentedControl from "./SegmentedControl.vue";
import StudentCard from "./StudentCard.vue";
import {useStudentStore} from "../stores/useStudentStore";
import stati from "../features/mails/Status";
import {useQuasar} from "quasar";
import {Student} from '../models/Student';
import {useSkillStore} from "../stores/useSkillStore";
import StudentSkillChip from "../features/students/components/StudentSkillChip.vue";
import { wsBaseUrl } from '../utils/baseUrl';
import { useProjectStore } from '../stores/useProjectStore';

export default defineComponent({
  name: 'SideBar',
  components: {
    StudentSkillChip,
    StudentCard,
    SegmentedControl,
  },
  setup() {
    const studentStore = useStudentStore()
    const skillStore = useSkillStore()
    const projectStore = useProjectStore()

    const $q = useQuasar()

    return {
      studentStore,
      skillStore,
      projectStore,
      $q,
      thumbStyle: {
        right: '0px',
        borderRadius: '7px',
        backgroundColor: 'black',
        width: '4px',
      },
      stati,
      socket: new WebSocket(wsBaseUrl),
    }
  },
  data() {
    return {
      miniState: ref(false),
      showFilters: ref(false),
      showShadow: ref(false),
      search: ref(''),
      alumni: ref('all'),
      suggestion: ref('none'),
      byMe: ref('maybe'),
      onProject: ref('maybe'),
      status: ref(''),
      skills: ref([])
    }
  },
  computed: {
    onProjectsPage(): boolean {
      return this.$route.name === "Projects"
    },
    onStudentsPage(): boolean {
      return this.$route.name === "Students" || this.$route.name === "Student Page";
    },
    filters() {
      let filter = {} as {
        search: string
        alum: boolean
        student_coach: boolean
        suggestion: string
        suggested_by_user: string
        on_project: string
        status: string
        skills: Array<number>
      }

      if (this.search) filter.search = this.search
      if (this.alumni === 'alumni') filter.alum = true
      if (this.alumni === 'student coaches') filter.student_coach = true
      if (this.suggestion !== 'none') filter.suggestion = this.suggestion
      if (this.byMe !== 'maybe') filter.suggested_by_user = this.byMe
      if (this.onProject !== 'maybe') filter.on_project = this.onProject
      if (this.status) filter.status = this.status
      if (this.skills.length > 0) filter.skills = this.skills.map((skill: { id: number }) => skill.id)

      return filter
    },
    showDrawer(): boolean {
      return this.onProjectsPage || this.onStudentsPage
    }
  },
  async mounted() {
    await this.skillStore.loadSkills()

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
        this.projectStore.receiveSuggestion(data.suggest_student, this.onProject)
      else if (data.hasOwnProperty('remove_student'))
        this.projectStore.removeReceivedSuggestion(data.remove_student, this.onProject)
    }
  },
  methods: {
    // Saves the component id and user name in the dataTransfer.
    /**
     * Saves the component id and user name in the dataTransfer.
     * @param e drag event
     * @param item item being dragged
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onDragStart(e: any, item: any) {
      const data = {
        targetId: e.target.id,
        student: item
      }
      e.dataTransfer.setData(data.student.id, JSON.stringify(data))
      e.dataTransfer.dropEffect = 'copy'
      e.dataTransfer.effectAllowed = 'copy'
    },
    /**
     * Load all students and make the infinite scroll reload
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async loadStudents(scroll: any) {
      scroll.reset()
      scroll.resume()
      scroll.trigger()
    },
  }
})
</script>

<style scoped>
:deep(.q-card) {
  border-radius: 10px !important;
}

:deep(.q-item) {
  padding: 8px 8px !important;
}
</style>
