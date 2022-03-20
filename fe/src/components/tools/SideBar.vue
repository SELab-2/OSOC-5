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
      class="bg-grey-3 full-height"
    >
      <div :style="drawer && !miniState? '' : 'display: none'" class="fit full-height">
        <div class="">
          <div class="absolute-full q-ma-sm column q-gutter-y-sm">
            <h class="text-bold text-h5">Filters</h>

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

            <SegmentedControl
              color="primary"
              text-color="white"
              v-model="roleFilter"
              :options="[
                { name: 'all', label: 'All' },
                { name: 'alumni', label: 'Alumni' },
                { name: 'studentCoaches', label: 'Student Coaches' },
              ]"
            />

            <SegmentedControl
              color="primary"
              v-model="suggestion"
              :options="[
                { name: 'yes', label: 'Yes' },
                { name: 'maybe', label: 'Maybe' },
                { name: 'no', label: 'No' },
                { name: 'none', label: 'None' },
              ]"
            />

            <q-select
              rounded
              outlined
              dense
              v-model="roles"
              multiple
              color="primary"
              bg-color="white"
              :options="[
                { name: 'fullStack', label: 'Full-stack developer'},
                { name: 'data', label: 'Data person'},
                { name: 'frontend', label: 'Front-end developer'}
              ]"
              label="Roles"
            />

            <div class="row q-gutter-x-md">
              <q-checkbox
                color="primary"
                v-model="byMe"
                label="Suggested by you"
                right-label
              />
              <q-checkbox
                color="primary"
                v-model="onProject"
                label="On project"
                right-label
              />
            </div>

            <h class="text-bold text-h5">Students</h>
            <q-scroll-area class="scroll fadeOut" :thumb-style="thumbStyle" style="flex: 1 1 auto;">
              <q-list
                
                @dragenter="onDragEnter"
                @dragleave="onDragLeave"
                @dragover="onDragOver"
                @drop="onDrop"
                >
                <q-item v-for="student in students" 
                    :key="student.name" 
                    draggable="true"
                    @dragstart="onDragStart($event, student.name)"
                    :id="student.name">
                  <StudentCard
                    :name="student.name"
                    :yes="student.yes"
                    :maybe="student.maybe"
                    :no="student.no"
                    :official="student.official"
                    
                  />
                </q-item>
              </q-list>
            </q-scroll-area>

          </div>


        </div>


      </div>

      <!--
        in this case, we use a button (can be anything)
        so that user can switch back
        to mini-mode
      -->
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

<script lang="ts">
import {ref} from 'vue'
import SegmentedControl from "../SegmentedControl.vue";
import StudentCard from "./StudentCard.vue";

export default {
  methods: {
    onDragStart(e, item) {
      const data = {
        targetId: e.target.id,
        name: item
      }
      e.dataTransfer.setData('text', JSON.stringify(data))
      console.log(e.dataTransfer.getData('text'))
      e.dataTransfer.dropEffect = 'copy'
    },
    onDragEnter(e) {
      // don't drop on other draggables
      console.log(e.target.draggable)
      if (e.target.draggable !== true) {
        e.target.classList.add('drag-enter')
      }
    },
    onDragLeave(e) {
      e.target.classList.remove('drag-enter')
    },
    onDragOver(e) {
      e.preventDefault()
    },
    onDrop(e) {
      e.preventDefault()
      console.log(e)
    
      // don't drop on other draggables
      if (e.target.draggable === true) {
        return
      }
      const data = JSON.parse(e.dataTransfer.getData('text'))
      const draggedId = data.targetId
      const draggedEl = document.getElementById(draggedId)
      const name = data.name
      console.log(name)
      console.log(draggedEl)
    
      // check if original parent node
      if (draggedEl.parentNode === e.target) {
        e.target.classList.remove('drag-enter')
        return
      }
    
      // make the exchange
      draggedEl.parentNode.removeChild(draggedEl)
      e.target.appendChild(draggedEl)
      e.target.classList.remove('drag-enter')
    }
  },
  data() {

    return {
      drawer: ref(false),
      miniState: ref(false),
      roleFilter: ref('all'),
      suggestion: ref('yes'),
      search: ref(""),
      byMe: ref(false),
      onProject: ref(false),
      students: [
        {name: 'Charlie Delta', yes: 2, maybe: 3, no: 1, official: 'yes'},
        {name: 'Charlie Puth', yes: 8, maybe: 3, no: 1, official: 'maybe'},
        {name: 'Charlie Choplin', yes: 0, maybe: 3, no: 1, official: 'no'},
        {name: 'Charliee', yes: 3, maybe: 3, no: 5, official: 'no'},
        {name: 'Charlieee', yes: 3, maybe: 3, no: 5, official: 'no'},
        {name: 'Charlie', yes: 3, maybe: 3, no: 5, official: 'no'}
      ],
      thumbStyle: {
        right: '1px',
        borderRadius: '3px',
        width: '4px',
        opacity: '0.75'
      }
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