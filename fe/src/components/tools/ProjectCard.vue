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

      <div class="text-caption text-grey">Roles:</div>
      <project-role-chip
        v-model="this.selectedRoles[role.type]"
        v-for="(role, index) in project.roles"
        @dragenter="onDragEnter($event, role)"
        @dragleave="onDragLeave($event, role)"
        @dragover="this.amountLeft(role) > 0 ? onDragOver($event, role) : ''"
        @drop="onDrop($event, role)"
        :key="index"
        :role="role"
        :placesLeft="amountLeft(role)"
      />

      <q-slide-transition v-for="(role, index) in project.roles" :key="index" style="margin-top: 15px; margin-bottom: -15px;">
        <div v-show="this.selectedRoles[role.type]" >
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
                <q-btn
                  class="gt-xs"
                  size="sm"
                  flat
                  dense
                  round
                  icon="comment"
                />
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
  props: {
    project: {},
  },
  setup(props) {
    return {
        
      selectedRoles: reactive(
        Object.assign(
          ...props.project.roles.map((role) => ({ [role.type]: false }))
        )
      ),
    }
  },
  components: { ProjectRoleChip },
  methods: {
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
    onDragEnter(e, role) {
        
      // don't drop on other draggables
      if (e.target.draggable !== true) {
        e.target.classList.add('drag-enter')
        e.stopPropagation();
        console.log("Entered!")
        
      }
      this.test += 1
      console.log(test)
      
    },
    onDragLeave(e, role) {
        e.stopPropagation();
        console.log("Left!")
        this.test -= 1
          console.log(test)
      e.target.classList.remove('drag-enter')
      this.selectedRoles[role.type] = false
    },
    amountLeft(role) {
        const occupied = this.groupedStudents[role.type]
        console.log(occupied)
        return this.project.roles.find(role => role.type === role.type).amount - (occupied ? occupied.length : 0)
    },
    onDragOver(e, role) {
        console.log("Over")
      e.preventDefault()
      e.stopPropagation();
      this.selectedRoles[role.type] = true
    },
    async onDrop(e, role) {
      e.preventDefault()
      console.log(e)

      // don't drop on other draggables
      if (e.target.draggable === true) {
        return
      }
      const data = JSON.parse(e.dataTransfer.getData('text'))
      console.log(data)
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
      
      // e.target.appendChild(draggedEl)
      e.target.classList.remove('drag-enter')
      console.log(role)
      this.project.students.push({ id: 10, name: name, role: role.type })
      draggedEl.parentNode.removeChild(draggedEl)
      await nextTick()
      setTimeout(() => this.selectedRoles[role.type] = false, 1000)
      
    },
  },
  computed: {
    groupedStudents() {
      let students = this.groupBy(this.project.students, 'role')
      return students
    },
    
  },
}
</script>

<style></style>
