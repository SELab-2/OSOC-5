<template>
  <q-card class="my-card shadow-4 q-ma-sm" flat bordered>
    <q-card-section>
      <div class="row">
        <div class="col">
          <div class="text-h5 text-bold q-mt-sm q-mb-xs">
            {{ project.name }}
          </div>
          <div class="text-overline">{{ project.partnerName }}</div>
        </div>
        <div>
          <q-btn flat round size="12px" color="primary" icon="mail" />
          <q-btn flat round size="12px" color="primary" icon="info" />
          <q-btn flat round size="12px" color="primary" icon="edit" />
        </div>
      </div>
      <div class="text-caption text-grey">Coaches:</div>
      <q-chip v-for="coach in project.coaches" :key="coach.id" icon="person">
        {{ coach.firstName }} {{ coach.lastName.split(" ").map(res => res.charAt(0)).join("") }}.
      </q-chip>

      <div
        class="row"
        style="display: flex; align-items: center"
        @click="this.expanded = !this.expanded; toggleExpanded(this.expanded)"
      >
        <div class="text-caption text-grey">Roles:</div>
        <q-btn flat round size="sm" icon="mdi-eye" />
      </div>
      <project-role-chip
        v-model="this.selectedRoles[role.skill.id]"
        v-for="(role, index) in project.requiredSkills"
        @dragleave="onDragLeave($event, role)"
        @dragover="this.amountLeft(role) > 0 ? onDragOver($event, role) : ''"
        @drop="onDrop($event, role)"
        :key="index"
        :role="role.skill"
        :placesLeft="amountLeft(role)"
      />

      <q-slide-transition
        v-for="(role, index) in project.requiredSkills"
        :key="index"
        style="margin-top: 10px; margin-bottom: -10px"
      >
        <div v-show="this.selectedRoles[role.skill.id]">
          <q-item-label
            class="text-subtitle1 text-bold"
            :class="'text-' + role.skill.color + '-8'"
          >
            {{ role.skill.name }}
          </q-item-label>
          <q-item
            dense
            v-for="suggestion in groupedStudents[role.skill.id]"
            :key="suggestion.student.id"
          >
            <q-item-section lines="1" class="text-weight-medium">
              {{ suggestion.student.firstName}} {{ suggestion.student.lastName }}
            </q-item-section>

            <div class="text-grey-8">
              <q-btn class="gt-xs" size="sm" flat dense round icon="comment" />
              <q-btn class="gt-xs" size="sm" flat dense round icon="info" />
              <q-btn class="gt-xs" size="sm" flat dense round icon="delete" @click="removeSuggestion(suggestion)"/>
            </div>
          </q-item>
        </div>
      </q-slide-transition>
    </q-card-section>
  </q-card>
</template>

<script>
import ProjectRoleChip from './ProjectRoleChip.vue'
import { useProjectStore } from "../../../stores/useProjectStore"
import { reactive, ref, nextTick } from 'vue'
import { useQuasar } from 'quasar'


var test = 0
export default {
  props: { project: {} },
  components: { ProjectRoleChip },
  setup() {
    return {
      $q: useQuasar(),
      projectStore: useProjectStore()
    }
  },

  data() {
    console.log(this.project.requiredSkills.map(role => role.skill))
    return {
      expanded: ref(false),
      selectedRoles: reactive(
        Object.assign(
          ...this.project.requiredSkills.map((role) => ({ [role.skill.id]: false }))
        )
      ),
    }
  },

  methods: {
    // Expand/Hide the whole student list.
    toggleExpanded(state) {
      Object.keys(this.selectedRoles).forEach(
        (role) => (this.selectedRoles[role] = state)
      )
    },

    groupBy(array, key) {
      const result = {}
      array.forEach((item) => {
        if (!result[item[key]]) {
          result[item[key]] = []
        }
        result[item[key]].push(item)
      })
      return result
    },
    
    removeSuggestion(suggestion) {
      const i = this.project.suggestedStudents.findIndex(s => s.student.id === suggestion.student.id && s.skill.id === suggestion.skill.id)
      console.log(i)
      this.project.suggestedStudents.splice(i,1)
      this.projectStore
        .removeSuggestion(this.project, suggestion)
        .catch(error => {
            this.$q.notify({
              icon: 'warning',
              color: 'warning',
              message: `Error ${error.response.status} while removing ${suggestion.student.firstName} ${suggestion.student.lastName} as ${suggestion.role.name}`,
              textColor: 'black'
            });
            this.project.suggestedStudents.splice(i, 0, suggestion)
          }
        )
    },

    // Calculates how many places of a role are occupied.
    amountLeft(role) {
      const occupied = this.groupedStudents[role.skill.id]
      return role.amount - (occupied ? occupied.length : 0)
    },

    // Show the students assigned to a role when dragging over the chip of that role.
    onDragOver(e, role) {
      e.preventDefault()
      e.stopPropagation()
      this.selectedRoles[role.skill.id] = true
    },

    // Hide the students assigned to a role when dragging away from the chip of that role.
    onDragLeave(e, role) {
      e.target.classList.remove('drag-enter')
      if (!this.expanded) {
        this.selectedRoles[role.skill.id] = false
      }
    },

    // Assign a student to a role.
    async onDrop(e, role) {
      e.preventDefault()

      // don't drop on other draggables
      if (e.target.draggable === true) {
        return
      }
      const data = JSON.parse(e.dataTransfer.getData('text'))
      const draggedEl = document.getElementById(data.targetId)
      console.log(data)
      // Add a student to the project and remove the student card from the sidebar.
      e.target.classList.remove('drag-enter')
      const reason = "mimimi"
      let result = await this.projectStore.addSuggestion(this.project.id, data.student.url, role.skill.url, reason)
      console.log(result)
      this.project.suggestedStudents.push({coach:undefined, reason: reason, skill: role.skill, student: data.student})
      draggedEl.parentNode.removeChild(draggedEl)

      // Hide the expanded list after dragging. If the list was already expanded by the user, don't hide it.
      if (!this.expanded) {
        setTimeout(() => (this.selectedRoles[role.skill.id] = false), 1000)
      }
    },
  },
  computed: {
    // Groups the students by role.
    // Example: { 'backend' : [{student1}, {student2}] }
    groupedStudents() {
      const result = {}
      this.project.suggestedStudents.forEach(student => {
        if (!result[student.skill.id]) {
          result[student.skill.id] = []
        }
        result[student.skill.id].push(student)
      })
      return result
      // console.log(this.groupBy(this.project.suggestedStudents, 'role.id'))
      // return this.groupBy(this.project.suggestedStudents, 'role.id')
    },
  },
}
</script>
