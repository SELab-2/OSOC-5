<template>
  <!-- <q-page-container style="height: 100%"> -->

  <div>
    <div class="q-pa-lg full-height flex-center">
      <label>Select a student from the sidebar to get started</label>
    </div>
  </div>
  <!-- </q-page-container> -->
</template>

<script lang="ts">
import {ref} from "vue"
import SideBar from "../../components/SideBar.vue"
import {defineComponent} from "@vue/runtime-core";
import { Student } from "../../models/Student";

export default defineComponent({
  components: {
    SideBar,
  },
  setup() {
    const student = ref(null)

    return {
      student,
    }
  },
  methods: {
    selectStudent: function (selected_student: Student) {
      this.$router.push(`/students/${selected_student.id}`)
    },
  }
})
</script>

<style>
.minimum_width {
  min-width: 300px !important;
}

.studentcol {
  padding: 5px;
}

.cornered {
  border-radius: 10px !important
}
</style>
