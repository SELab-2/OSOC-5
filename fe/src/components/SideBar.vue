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
              v-model="studentStore.search"
              outlined
              dense
              rounded
              debounce="300"
              color="green"
              bg-color="white"
              label="Search"
              @update:modelValue="() => loadStudents($refs.infiniteScroll)"
            >
              <template #append>
                <q-icon name="search" />
              </template>
            </q-input>

            <SegmentedControl
              v-model="studentStore.alumni"
              color="primary"
              text-color="white"
              :options="[
                { name: 'all', label: 'All' },
                { name: 'alumni', label: 'Alumni' },
                { name: 'student coaches', label: 'Student Coaches'}
              ]"
              @click="() => loadStudents($refs.infiniteScroll)"
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
              @click="() => loadStudents($refs.infiniteScroll)"
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
              @update:model-value="() => loadStudents($refs.infiniteScroll)"
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
              @update:model-value="() => loadStudents($refs.infiniteScroll)"
            />

            <div class="row q-gutter-x-md">
              <q-checkbox
                v-model="studentStore.byMe"
                toggle-indeterminate
                checked-icon="mdi-check"
                true-value="true"
                unchecked-icon="mdi-minus-thick"
                false-value="false"
                indeterminate-icon="mdi-help"
                indeterminate-value="maybe"
                toggle-order="tf"
                color="primary"
                label="Suggested by you"
                right-label
                @click="() => loadStudents($refs.infiniteScroll)"
              />
              <q-checkbox
                v-model="studentStore.onProject"
                toggle-indeterminate
                checked-icon="mdi-check"
                true-value="true"
                unchecked-icon="mdi-minus-thick"
                false-value="false"
                indeterminate-icon="mdi-help"
                indeterminate-value="maybe"
                toggle-order="tf"
                color="primary"
                label="On project"
                right-label
                @click="() => loadStudents($refs.infiniteScroll)"
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
              <q-infinite-scroll
                :key="scrollKey"
                ref="infiniteScroll"
                class="q-px-sm"
                :offset="250"
                @load="(index, done) => studentStore.loadNext(index, done)"
              >
                <StudentCard
                  v-for="student in studentStore.students"
                  :id="student.email"
                  :key="student.email"
                  v-ripple
                  class="q-ma-sm"
                  :draggable="draggable ?? false"
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
        </div>
      </div>

      <div
        class="absolute"
        style="top: 15px; right: -17px"
      >
        <btn
          dense
          round
          style="border-radius: 30px;"
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
  props: {
    clickable: {
      type: Boolean,
      required: false,
      default: false
    },
    color: {
      type: String,
      required: true
    },
    draggable: {
      type: Boolean,
      required: false
    },
    mustHover: {
      type: Boolean,
      required: true
    }
  },
  setup() {
    const studentStore = useStudentStore()
    const skillStore = useSkillStore()

    const $q = useQuasar()

    return {
      studentStore,
      skillStore,
      $q,
      thumbStyle: {
        right: '0px',
        borderRadius: '7px',
        backgroundColor: 'black',
        width: '4px',
      },
      status,
      scrollKey: 0
    }
  },
  data() {
    return {
      miniState: ref(false),
      drawer: ref(true),
    }
  },
  created() {
    // load all students
    this.studentStore.loadStudents()
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
      e.dataTransfer.setData(data.student.id, JSON.stringify(data))
      e.dataTransfer.dropEffect = 'copy'
      e.dataTransfer.effectAllowed = 'copy'
    },
    /**
     * Clicking a student sets the selected student of the sidebar
     * @param student the clicked student in the sidebar
     */
    clickStudent(student: Student) {
      this.selectStudent(student)
    },
    /**
     * Load all students and make the infinite scroll reload
     */
    loadStudents(scroll: any) {
      scroll.resume()
      this.studentStore.loadStudents()
      this.scrollKey += 1
    },
    /**
     * Route to the correct details page of selected_student
     * @param selected_student student to be displayed
     */
    selectStudent: function (selected_student: Student) {
      this.$router.push(`/students/${selected_student.id}`)
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

::-webkit-scrollbar {
  width: 4px;
}

::-webkit-scrollbar-thumb {
  right: 0px;
  background-color: darkgray;
  border-radius: 7px;
  width: 4px;
  opacity: 0.75;
}
</style>
