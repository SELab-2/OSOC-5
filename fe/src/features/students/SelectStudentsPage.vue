<template>
  <div>
    <SideBar :selectStudent="selectStudent" :draggable="false"/>
    <div class="q-pa-lg full-height flex-center">
      <label>Select a student from the sidebar to get started</label>
    </div>
  </div>
</template>

<script>
import {ref} from "vue"
import SideBar from "../../components/SideBar.vue"

export default {
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
    selectStudent: function (selected_student) {
      this.$router.push(`/students/${selected_student.id}`)
    },
  }
}
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