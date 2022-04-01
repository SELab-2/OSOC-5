<template>
  <div>
    <SideBar :selectStudent="selectStudent" :draggable="false"/>
    <div v-if="!this.student" class="q-pa-lg full-height flex-center">
      <label>Select a student from the sidebar to get started</label>
    </div>

    <div v-if="this.student">
      <StudentPage :student="this.student" />
    </div>
  </div>
</template>

<script>
import {ref} from "vue"
import {openURL, useQuasar} from 'quasar'
import SideBar from "../../components/SideBar.vue"
import SegmentedControl from "../../components/SegmentedControl.vue";
import StudentCard from "../../components/StudentCard.vue";
import TitleTextCard from "./components/TitleTextCard.vue";
import SuggestionsCard from "./components/SuggestionsCard.vue";
import PracticalCard from "./components/PracticalCard.vue";
import DetailsCard from "./components/DetailsCard.vue";
import AcademiaCard from "./components/AcademiaCard.vue";
import {useAuthenticationStore} from "../../stores/useAuthenticationStore"
import {useStudentStore} from "../../stores/useStudentStore";
import StudentPage from "./StudentPage.vue";

export default {
  components: {
    SideBar,
    StudentPage
  },
  setup() {
    const student = ref(null)

    return {
      student,
    }
  },
  methods: {
    selectStudent: function (selected_student) {
      this.student = selected_student
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