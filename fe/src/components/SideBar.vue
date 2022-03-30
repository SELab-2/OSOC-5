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
      class="bg-grey-3 full-height"
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
              placeholder="Search"
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
            />

            <SegmentedControl
              v-model="suggestion"
              color="primary"
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
                v-model="byMe"
                color="primary"
                label="Suggested by you"
                right-label
              />
              <q-checkbox
                v-model="onProject"
                color="primary"
                label="On project"
                right-label
              />
            </div>

            <div class="text-bold text-h5">
              Students
            </div>
            <q-scroll-area
              class="scroll fadeOut"
              :thumb-style="thumbStyle"
              style="flex: 1 1 auto;"
            >
              <q-list>
                <q-item
                  v-for="student in students" 
                  :id="student.name" 
                  :key="student.name"
                  draggable="true"
                  @dragstart="onDragStart($event, student.name)"
                >
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

export default defineComponent({
  components: {
    StudentCard,
    SegmentedControl,
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
      students: [
        {name: 'Charlie Delta', yes: 2, maybe: 3, no: 1, official: 'yes'},
        {name: 'Echo Sierra', yes: 8, maybe: 3, no: 1, official: 'maybe'},
        {name: 'November Quebec', yes: 0, maybe: 3, no: 1, official: 'no'},
        {name: 'Charles Callender', yes: 3, maybe: 3, no: 5, official: 'maybe'},
        {name: 'Ressie Rosser', yes: 0, maybe: 1, no: 5, official: 'yes'},
        {name: 'Jane Johnson', yes: 3, maybe: 3, no: 5, official: 'no'}
      ]
    }
  },
  methods: {
    // Saves the component id and user name in the dataTransfer.
    // TODO: send id of user instead of name.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    onDragStart(e: any, item: any) {
      const data = {
        targetId: e.target.id,
        name: item
      }
      e.dataTransfer.setData('text', JSON.stringify(data))
      e.dataTransfer.dropEffect = 'copy'
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