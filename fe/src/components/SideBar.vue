<template>
  <div >
    <q-drawer
      v-model="drawer"
      show-if-above
      :mini="!drawer || miniState"
      :mini-width="30"
      :width="350"
      :breakpoint="100"
      bordered
      class="full-height"
      :class="this.color"
    >
      <div :style="drawer && !miniState? '' : 'display: none'" class="fit full-height">
        <div class="">
          <div class="absolute-full q-ma-sm column q-gutter-y-sm">
            <div class="text-bold text-h5">Filters</div>

            <q-input
              outlined
              dense
              rounded
              debounce="300"
              color="green"
              bg-color="white"
              v-model="search"
              label="Search by name..."
              @keydown.enter="fetchStudents"
            >
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

            <SegmentedControl
              color="primary"
              text-color="white"
              v-model="roleFilter"
              :options="[
                { name: 'all', label: 'All' },
                { name: 'alumni', label: 'Alumni' },
                { name: 'studentCoaches', label: 'Student Coaches' },
              ]"
              @click="fetchStudents"
            />

            <label>Suggestion:</label>
            <SegmentedControl
              color="primary"
              v-model="suggestion"
              :options="[
                { name: 'yes', label: 'Yes' },
                { name: 'maybe', label: 'Maybe' },
                { name: 'no', label: 'No' },
                { name: 'none', label: 'None' },
              ]"
              @click="fetchStudents"
            />

            <q-select
              rounded
              outlined
              dense
              multiple
              v-model="roles"
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
                color="primary"
                v-model="byMe"
                label="Suggested by you"
                right-label
                @click="fetchStudents"
              />
              <q-checkbox
                color="primary"
                v-model="onProject"
                label="On project"
                right-label
                @click="fetchStudents"
              />
            </div>

            <div class="text-bold text-h5">Students</div>
            <q-scroll-area class="scroll fadeOut" :thumb-style="thumbStyle" style="flex: 1 1 auto;">
              <q-list>
                <q-item v-for="student in studentStore.students"
                    :key="student.name" 
                    :draggable="this.draggable"
                    @dragstart="onDragStart($event, student.name)"
                    :id="student.name">
                  <StudentCard
                    clickable
                    v-ripple
                    :student="student"
                    @click="this.selectStudent(student)"
                  />
                </q-item>
              </q-list>
            </q-scroll-area>

          </div>


        </div>


      </div>

      <div class="absolute" style="top: 15px; right: -17px">
        <q-btn
          dense
          round
          unelevated
          color="yellow"
          :icon="drawer && !miniState? 'chevron_left' : 'chevron_right'"
          @click="this.miniState = !this.miniState"
        />
      </div>
    </q-drawer>
  </div>
</template>

<script>
import {ref} from 'vue'
import SegmentedControl from "./SegmentedControl.vue";
import StudentCard from "./StudentCard.vue";
import {useStudentStore} from "../stores/useStudentStore";
import {useQuasar} from "quasar";
import {onMounted} from "@vue/runtime-core";

export default {
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
    }
  },
  methods: {
    // Saves the component id and user name in the dataTransfer.
    // TODO: send id of user instead of name.
    onDragStart(e, item) {
      const data = {
        targetId: e.target.id,
        name: item
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
  components: {
    StudentCard,
    SegmentedControl,
  }
}
</script>

<style scoped>
:deep(.q-card) {
    border-radius: 10px !important;
  }
  
:deep(.q-item) {
  padding: 8px 8px !important;
}
</style>