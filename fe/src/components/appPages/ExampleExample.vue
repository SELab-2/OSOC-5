<template>
  <div>
    <q-drawer
        v-model="drawer"
        show-if-above

        :mini="!drawer || miniState"
        @click.capture="drawerClick"

        :mini-width="30"
        :width="300"
        :breakpoint="100"
        bordered
        class="bg-grey-3"
    >
      <q-scroll-area class="fit">
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
import { ref } from 'vue'

export default {
  setup () {
    const miniState = ref(false)
    const drawer = ref(false)

    return {
      drawer,
      miniState,

      drawerClick (e) {
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
  }
}
</script>