<template>
  <div>
    <q-drawer
      v-model="drawer"
      show-if-above
      :mini="!drawer || miniState"
      :mini-width="30"
      :width="350"
      :breakpoint="100"
      bordered
      class="full-height"
      :class="color"
    >
      <div
        :style="drawer && !miniState? '' : 'display: none'"
        class="fit full-height"
      >
        <div class="">
          <div class="absolute-full q-ma-sm column q-gutter-y-sm">
            <div class="text-bold text-h5">
              Filters
            </div>

            <q-input
              v-model="this.studentStore.search"
              outlined
              dense
              rounded
              debounce="300"
              color="green"
              bg-color="white"
              label="Search by name..."
              @keydown.enter="fetchStudents"
            >
              <template #append>
                <q-icon name="search" />
              </template>
            </q-input>

            <SegmentedControl
              v-model="this.studentStore.alumni"
              color="primary"
              text-color="white"
              :options="[
                { name: 'all', label: 'All' },
                { name: 'alumni', label: 'Alumni' },
              ]"
              @click="fetchStudents"
            />

            <label>Suggestion:</label>
            <SegmentedControl
              v-model="this.studentStore.decision"
              color="primary"
              :options="[
                { name: 'yes', label: 'Yes' },
                { name: 'maybe', label: 'Maybe' },
                { name: 'no', label: 'No' },
                { name: 'none', label: 'None' },
              ]"
              @click="fetchStudents"
            />

            <q-select
              v-model="studentStore.skills"
              rounded
              outlined
              dense
              multiple
              virtual-scroll-slice-size="5"
              color="primary"
              bg-color="white"
              :options="skillStore.skills"
              :option-label="opt => opt.name"
              :option-value="opt => opt.id"
              label="Roles"
              @update:model-value="fetchStudents"
            >
              <template #selected>
                <div class="column">
                  <StudentSkillChip
                    v-for="skill of studentStore.skills"
                    :key="skill.id"
                    :color="skill.color"
                    :name="skill.name"
                  />
                </div>
              </template>
            </q-select>

            <div class="row q-gutter-x-md">
              <q-checkbox
                v-model="studentStore.byMe"
                color="primary"
                label="Suggested by you"
                right-label
                @click="fetchStudents"
              />
              <q-checkbox
                v-model="this.studentStore.onProject"
                color="primary"
                label="On project"
                right-label
                @click="fetchStudents"
              />
            </div>

            <div class="text-bold text-h5">
              Students
            </div>
            <q-scroll-area
              class=" fadeOut"
              :thumb-style="thumbStyle"
              style="flex: 1 1 auto"
            >
              <q-list>
                <q-item
                  v-for="student in studentStore.students"
                  :id="student.email"
                  :key="student.email"
                  :draggable="draggable"
                  @dragstart="onDragStart($event, student)"
                >
                  <StudentCard
                    v-ripple
                    :student="student"
                    :active="this.student ? student.email === this.student.email : false"
                    @click="this.clickStudent(student)"
                  />
                </q-item>
              </q-list>
            </q-scroll-area>
          </div>
        </div>
      </div>

      <div
        class="absolute"
        style="top: 15px; right: -17px"
      >
        <q-btn
          dense
          round
          unelevated
          color="yellow"
          :icon="drawer && !miniState? 'chevron_left' : 'chevron_right'"
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
import {useQuasar} from "quasar";
import {onMounted} from "@vue/runtime-core";
import { Student } from '../models/Student';
import {useSkillStore} from "../stores/useSkillStore";
import StudentSkillChip from "../features/students/components/StudentSkillChip.vue";

export default defineComponent({
  components: {
    StudentSkillChip,
    StudentCard,
    SegmentedControl,
  },
  props: {
    selectStudent: {
      type: Function,
      required: true
    },
    color: {
      type: String,
      required: true
    },
    draggable: {
      type: Boolean,
      required: true
    },
    student: {
      type: Student,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()
    const skillStore = useSkillStore()
    const $q = useQuasar()

    onMounted(() => {
      studentStore.loadStudents()
      skillStore.loadSkills()
    })

    return {
      studentStore,
      skillStore,
      $q,
      thumbStyle: {
        right: '0px',
        borderRadius: '7px',
        backgroundColor: 'black',
        width: '4px',
        opacity: 0.75
      },
    }
  },
  data() {
    return {
      miniState: ref(false),
      drawer: ref(false),
      roles: ref([]),
    }
  },
  methods: {
    // Saves the component id and user name in the dataTransfer.
    // TODO: send id of user instead of name.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onDragStart(e: any, item: any) {
      const data = {
        targetId: e.target.id,
        student: item
      }
      e.dataTransfer.setData('text', JSON.stringify(data))
      e.dataTransfer.dropEffect = 'copy'
    },
    fetchStudents() {
      this.studentStore.loadStudents()
    },
    clickStudent(student: Student) {
      this.selectStudent(student)
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