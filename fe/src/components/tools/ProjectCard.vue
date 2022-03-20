<template>
  <q-card class="my-card shadow-4 q-ma-sm" flat bordered>
    <q-card-section>
      <div class="row">
        <div class="col">
          <div class="text-h5 text-bold q-mt-sm q-mb-xs">
            {{ project.title }}
          </div>
          <div class="text-overline">{{ project.client }}</div>
        </div>
        <div>
          <q-btn flat round size="12px" color="primary" icon="mail" />
          <q-btn flat round size="12px" color="primary" icon="info" />
          <q-btn flat round size="12px" color="primary" icon="edit" />
        </div>
      </div>
      <div class="text-caption text-grey">Coaches:</div>
      <q-chip v-for="coach in project.coaches" :key="coach.id" icon="person">{{
        coach.name
      }}</q-chip>

      <div
        class="row"
        style="display: flex; align-items: center"
        @click="this.expanded = !this.expanded; toggleExpanded(this.expanded)"
      >
        <div class="text-caption text-grey">Roles:</div>
        <q-btn flat round size="sm" icon="mdi-eye" />
      </div>
      <project-role-chip
        v-model="this.selectedRoles[role.type]"
        v-for="(role, index) in project.roles"
        @dragleave="onDragLeave($event, role)"
        @dragover="this.amountLeft(role) > 0 ? onDragOver($event, role) : ''"
        @drop="onDrop($event, role)"
        :key="index"
        :role="role"
        :placesLeft="amountLeft(role)"
      />

      <q-slide-transition
        v-for="(role, index) in project.roles"
        :key="index"
        style="margin-top: 10px; margin-bottom: -10px"
      >
        <div v-show="this.selectedRoles[role.type]">
          <q-item-label
            class="text-subtitle1 text-bold"
            :class="'text-' + role.color + '-8'"
          >
            {{ role.label }}
          </q-item-label>
          <q-item
            dense
            v-for="student in groupedStudents[role.type]"
            :key="student.id"
          >
            <q-item-section lines="1" class="text-weight-medium">{{
              student.name
            }}</q-item-section>

            <div class="text-grey-8">
              <q-btn class="gt-xs" size="sm" flat dense round icon="comment" />
              <q-btn class="gt-xs" size="sm" flat dense round icon="info" />
              <q-btn class="gt-xs" size="sm" flat dense round icon="delete" />
            </div>
          </q-item>
        </div>
      </q-slide-transition>
    </q-card-section>
  </q-card>
</template>

<script>
import ProjectRoleChip from './ProjectRoleChip.vue'
import { reactive, ref, nextTick } from 'vue'

var test = 0
export default {
  props: { project: {} },
  components: { ProjectRoleChip },
  setup(props) {
    return {
      // Marks all role lists as hidden.
      selectedRoles: reactive(
        Object.assign(
          ...props.project.roles.map((role) => ({ [role.type]: false }))
        )
      ),
    }
  },

  data() {
    return {
      expanded: ref(false),
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

    // Calculates how many places of a role are occupied.
    amountLeft(role) {
      const occupied = this.groupedStudents[role.type]
      return role.amount - (occupied ? occupied.length : 0)
    },

    // Show the students assigned to a role when dragging over the chip of that role.
    onDragOver(e, role) {
      e.preventDefault()
      e.stopPropagation()
      this.selectedRoles[role.type] = true
    },

    // Hide the students assigned to a role when dragging away from the chip of that role.
    onDragLeave(e, role) {
      e.target.classList.remove('drag-enter')
      if (!this.expanded) {
        this.selectedRoles[role.type] = false
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

      // Add a student to the project and remove the student card from the sidebar.
      e.target.classList.remove('drag-enter')
      this.project.students.push({ id: 10, name: data.name, role: role.type })
      draggedEl.parentNode.removeChild(draggedEl)

      // Hide the expanded list after dragging. If the list was already expanded by the user, don't hide it.
      if (!this.expanded) {
        setTimeout(() => (this.selectedRoles[role.type] = false), 1000)
      }
    },
  },
  computed: {
    // Groups the students by role.
    // Example: { 'backend' : [{student1}, {student2}] }
    groupedStudents() {
      return this.groupBy(this.project.students, 'role')
    },
  },
}
</script>
