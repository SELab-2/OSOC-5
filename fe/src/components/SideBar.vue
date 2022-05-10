<template>
  <div>
    <q-drawer
      v-model="showDrawer"
      :mini="miniState"
      :mini-width="30"
      :width="350"
      :breakpoint="100"
      class="bg-grey-1 shadow-4"
    >
    <div
    :style="!miniState? '' : 'display: none'"
      style="height: 100%; overflow: hidden;"
      class="fit column"
    >
        
          <div :class="`${showShadow ? 'shadow-2' : ''}`" style="z-index: 1; transition: box-shadow ease 500ms" class="q-px-sm">
            <div class="text-bold text-h5 q-py-sm">
              Students
            </div>
            <div class="row no-wrap q-pb-sm">
            <q-input
              v-model="studentStore.search"
              @update:modelValue="async () => await loadStudents($refs.infiniteScroll)"
              debounce="300"
              class="fit q-mr-sm"
              dense
              outlined
              color="teal"
              label="Search Students"
              hide-bottom-space
            >
            <template v-slot:append>
              <q-icon name="search" color="teal-4" />
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
              <div v-if="showFilters" class="overflow-hidden">
                <!-- div needs to be wrapped because gutter produces negative margins, which cause issues with q-slide-transition -->
                <div class="q-gutter-y-sm q-px-xs">
                
            <SegmentedControl
              v-model="studentStore.alumni"
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
              v-model="studentStore.decision"
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
              v-model="studentStore.skills"
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
                    v-for="skill of studentStore.skills"
                    :key="skill.id"
                    :color="skill.color"
                    :name="skill.name"
                    best-skill=""
                  />
                </div>
              </template>
            </q-select>

            <q-select
              v-model="studentStore.status"
              rounded
              outlined
              dense
              clearable
              color="primary"
              bg-color="white"
              :options="status"
              :option-label="opt => opt.label"
              :option-value="opt => opt.value"
              label="Status"
              emit-value
              map-options
              @update:model-value="async () => await loadStudents($refs.infiniteScroll)"
            />

            <div class="row q-gutter-x-md">
              <q-checkbox
                v-model="studentStore.byMe"
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
                v-model="studentStore.onProject"
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
              style="flex: 1; overflow: auto;"
              @scroll="onScroll"
              
            >
              <q-infinite-scroll
                ref="infiniteScroll"
                class="q-pa-sm"
                
                :offset="250"
                @load="async (index, done) => await loadNextStudents(index, done)"
              >
                <StudentCard
                  v-for="student in studentStore.students"
                  :id="student.email"
                  :key="student.email"
                  
                  class="q-ma-sm"
                  :draggable="draggable"
                  :must-hover="mustHover"
                  :student="student"
                  :active="studentStore.currentStudent ? student.email === studentStore.currentStudent.email : false"
                  @click="clickStudent(student)"
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
        
      

        <q-inner-loading
          :showing="studentStore.isLoading"
          label="Please wait..."
          label-class="text-teal"
          label-style="font-size: 1.1em"
        />
      

      <div
        class="absolute"
        style="top: 15px; right: -17px; z-index: 2;"
      >
        <btn
          dense
          shadow-color="yellow"
          shadow-strength = "1"
          color="yellow"
          :icon="!miniState? 'chevron_left' : 'chevron_right'"
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
import status from "../features/mails/Status";
import {useQuasar} from "quasar";
import { Student } from '../models/Student';
import {useSkillStore} from "../stores/useSkillStore";
import StudentSkillChip from "../features/students/components/StudentSkillChip.vue";

export default defineComponent({
  components: {
    StudentSkillChip,
    StudentCard,
    SegmentedControl,
  },
  name: 'SideBar',
  props: {
    selectStudent: {
      type: Function,
      required: true
    },
    draggable: {
      type: Boolean,
      required: false,
      default: true
    },
    mustHover: {
      type: Boolean,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()
    const $q = useQuasar()

    const skillStore = useSkillStore()

    return {
      studentStore,
      $q,
      skillStore,
      thumbStyle: {
        right: '0px',
        borderRadius: '7px',
        backgroundColor: 'black',
        width: '4px',
      },
      status,
    }
  },
  data() {
    return {
      miniState: ref(false),
      showFilters: ref(false),
      showShadow: ref(false),
    }
  },
  async mounted() {
    //this.skillStore.loadSkills()
    await this.studentStore.loadStudents()
  }, 
  computed: {
    showDrawer() {
      console.log(this.$route.name)
        return this.$route.name === "Students" || this.$route.name === "Projects" || this.$route.name === "Student Page";
    }
  },
  methods: {
    onScroll(info) {
      console.log(info.verticalPosition)
      this.showShadow = info.verticalPosition > 5
    },
    // Saves the component id and user name in the dataTransfer.
    // TODO: send id of user instead of name.
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
    clickStudent(student: Student) {
      this.$router.push(`/students/${student.id}`)
    },
    async loadStudents(scroll: any) {
      scroll.resume()
      this.studentStore.students = []
      await this.studentStore.loadStudents()
    },
    async loadNextStudents(index: number, done: any) {
      await this.studentStore.loadNext(index, done)
    }
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
