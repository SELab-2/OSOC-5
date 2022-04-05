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
              v-model="search"
              outlined
              dense
              rounded
              debounce="300"
              color="green"
              bg-color="white"
              label="Search by name..."
              @keydown.enter="fetchStudents"
            >
              >
              <template #append>
                <q-icon name="search" />
              </template>
            </q-input>

            <SegmentedControl
              v-model="roleFilter"
              color="primary"
              text-color="white"
              :options="[
                { name: 'all', label: 'All' },
                { name: 'alumni', label: 'Alumni' },
                { name: 'studentCoaches', label: 'Student Coaches' },
              ]"
              @click="fetchStudents"
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
              @click="fetchStudents"
            />

            <q-select
              v-model="roles"
              rounded
              outlined
              dense
              multiple
              color="primary"
              bg-color="white"
              :options="[
                { name: 'fullStack', label: 'Full-stack developer'},
                { name: 'data', label: 'Data person'},
                { name: 'frontend', label: 'Front-end developer'}
              ]"
              label="Roles"
              @update:model-value="fetchStudents"
            />

            <div class="row q-gutter-x-md">
              <q-checkbox
                v-model="byMe"
                color="primary"
                label="Suggested by you"
                right-label
                @click="fetchStudents"
              />
              <q-checkbox
                v-model="onProject"
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
                    clickable
                    :student="student"
                    :active="active === student.email"
                    @click="clickStudent(student)"
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

export default defineComponent({
  components: {
    StudentCard,
    SegmentedControl,
  },
  props: [ 'selectStudent', 'color', 'draggable' ],
  setup() {
    const studentStore = useStudentStore()
    const $q = useQuasar()

    onMounted(() => {
      studentStore.loadStudents()
    })

    return {
      studentStore,
      $q,
      thumbStyle: {
        right: '0px',
        borderRadius: '7px',
        backgroundColor: 'black',
        width: '4px',
        opacity: 0.75
      },
      active: ref('')
    }
  },
  data() {
    return {
      miniState: ref(false),
      drawer: ref(false),
      search: ref(""),
      byMe: ref(false),
      onProject: ref(false),
      roleFilter: ref('all'),
      suggestion: ref('yes'),
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
      console.log(this.search)
      console.log(this.roleFilter)
      console.log(this.suggestion)
      console.log(this.roles)
      console.log(this.byMe)
      console.log(this.onProject)
    },
    clickStudent(student) {
      this.active = student.email
      this.selectStudent(student)
    }
  },
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