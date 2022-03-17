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
      <q-scroll-area :style="drawer && !miniState? '' : 'visibility: hidden'" class="fit">
        <div class="q-ma-md column">
          <h class="text-bold text-h4">Filters</h>
          <br/>
          <q-input
            outlined
            dense
            rounded
            debounce="300"
            color="green"
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
          <q-card class="my-card">
            <q-card-section rounded>
              <div class="row">
                <label class="text-bold">Charlie Delta</label>
              </div>
              <q-linear-progress :value="0.2" :buffer="0.5" reverse rounded>
              </q-linear-progress>
              <q-progress class="mt-2" :max="max" show-value>
                <q-progress-bar :value="value * (6 / 10)" variant="success"></q-progress-bar>
                <q-progress-bar :value="value * (2.5 / 10)" variant="warning"></q-progress-bar>
                <q-progress-bar :value="value * (1.5 / 10)" variant="danger"></q-progress-bar>
              </q-progress>
            </q-card-section>
          </q-card>
        </div>


      </q-scroll-area>

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

export default {
  setup() {
    const miniState = ref(false)
    const drawer = ref(false)
    const search = ref("")
    const byMe = ref(false)
    const onProject = ref(false)
    const roleFilter = ref('all')
    const suggestion = ref('yes')

    return {
      drawer,
      miniState,
      roleFilter,
      suggestion,
      search,
      byMe,
      onProject,
      drawerClick(e) {
        console.log(miniState.value);
        console.log(drawer.value);
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
    SegmentedControl,
  }
}
</script>