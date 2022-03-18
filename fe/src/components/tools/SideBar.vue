<template>
  <div>
    <q-drawer
      v-model="drawer"
      show-if-above

      :mini="!drawer || miniState"
      @click.capture="drawerClick"

      :mini-width="30"
      :width="350"
      :breakpoint="100"
      bordered
      class="bg-grey-3"
    >
      <div :style="drawer && !miniState? '' : 'visibility: hidden'" class="fit">
        <div class="q-ma-md column">
          <h class="text-bold text-h4">Filters</h>
          <br/>
          <q-input
            outlined
            dense
            rounded
            debounce="300"
            color="green"
            bg-color="white"
            v-model="search"
            placeholder="Search"
          >
            <template v-slot:append>
              <q-icon name="search"/>
            </template>
          </q-input>
          <br/>
          <SegmentedControl
            color="green"
            v-model="roleFilter"
            :options="[
              { name: 'all', label: 'All' },
              { name: 'alumni', label: 'Alumni' },
              { name: 'studentCoaches', label: 'Student Coaches' },
            ]"
          />
          <br/>
          <SegmentedControl
            color="green"
            v-model="suggestion"
            :options="[
              { name: 'yes', label: 'Yes' },
              { name: 'maybe', label: 'Maybe' },
              { name: 'no', label: 'No' },
              { name: 'none', label: 'None' },
            ]"
          />
          <br/>
          <q-select
            rounded
            outlined
            v-model="roles"
            multiple
            color="green"
            bg-color="white"
            :options="[
              { name: 'fullStack', label: 'Full-stack developer'},
              { name: 'data', label: 'Data person'},
              { name: 'frontend', label: 'Front-end developer'}
            ]"
            label="Roles"
          />
          <q-toggle
            color="green"
            v-model="byMe"
            label="Suggested by you"
            right-label
          />
          <q-toggle
            color="green"
            v-model="onProject"
            label="On project"
            right-label
          />

          <h class="text-bold text-h4">Students</h>

          <q-list>
            <q-item v-for="(student, index) in students" :key="index">
              <StudentCard
                :name="student.name"
                :yes="student.yes"
                :maybe="student.maybe"
                :no="student.no"
                :official="student.official"
              />
            </q-item>
          </q-list>
        </div>


      </div>

      <!--
        in this case, we use a button (can be anything)
        so that user can switch back
        to mini-mode
      -->
      <div class=" absolute" style="top: 15px; right: -17px">
        <q-btn
          dense
          round
          unelevated
          color="yellow"
          :icon="drawer && !miniState? 'chevron_left' : 'chevron_right'"
          @click="miniState = true"
        />
      </div>
    </q-drawer>
  </div>
</template>

<script lang="ts">
import {ref} from 'vue'
import SegmentedControl from "../SegmentedControl.vue";
import StudentCard from "./StudentCard.vue";

export default {
  setup() {
    const miniState = ref(false)
    const drawer = ref(false)
    const search = ref("")
    const byMe = ref(false)
    const onProject = ref(false)
    const roleFilter = ref('all')
    const suggestion = ref('yes')
    const students = [
      {name: 'Charlie Delta', yes: 2, maybe: 3, no: 1, official: 'yes'},
      {name: 'Charlie Puth', yes: 8, maybe: 3, no: 1, official: 'maybe'},
      {name: 'Charlie Choplin', yes: 0, maybe: 3, no: 1, official: 'no'},
      {name: 'Charlie', yes: 3, maybe: 3, no: 5, official: 'no'}
    ]

    return {
      drawer,
      miniState,
      roleFilter,
      suggestion,
      search,
      byMe,
      onProject,
      students,
      drawerClick(e) {
        // if in "mini" state and user
        // click on drawer, we switch it to "normal" mode
        if (miniState.value) {
          miniState.value = false

          // notice we have registered an event with capture flag;
          // we need to stop further propagation as this click is
          // intended for switching drawer to "normal" mode only
          e.stopPropagation()
        }
      }
    }
  },
  components: {
    StudentCard,
    SegmentedControl,
  }
}
</script>