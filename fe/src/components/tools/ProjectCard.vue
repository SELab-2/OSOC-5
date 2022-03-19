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
        :key="index"
        :role="role"
      />

      <q-slide-transition v-for="(role, index) in project.roles" :key="index">
        <div v-show="this.selectedRoles[role.type]">
          <q-card-section class="text-subitle2">
            {{ role.label }}
          </q-card-section>
          <q-card-section>
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
          </q-card-section>
        </div>
      </q-slide-transition>
    </q-card-section>
    <!-- <q-list dense bordered separator>
                <div v-for="(group, index) in groupedStudents" :key="index">
                    <q-item-label lines='1' header>
                        {{ this.project.roles.find(role => role.type === group[0].role).label }}
                    </q-item-label>
                    <q-item inset-level="0.3" dense v-for="student in group" :key="student.id">
                        <q-item-section lines='1' class='text-weight-medium'>{{ student.name }}</q-item-section>
                            <div class='text-grey-8'>
                                <q-btn class='gt-xs' size='sm' flat dense round icon='comment' />
                                <q-btn class='gt-xs' size='sm' flat dense round icon='info' />
                                <q-btn class='gt-xs' size='sm' flat dense round icon='delete' />
                            </div>
                    </q-item>
                </div>
        </q-list> -->
  </q-card>
</template>

<script>
import ProjectRoleChip from './ProjectRoleChip.vue'
import { reactive, ref } from 'vue'
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
      test: ref(false),
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
  },
  computed: {
    groupedStudents() {
      console.log(this.project)
      let students = this.groupBy(this.project.students, 'role')
      console.log('Hello')
      console.log(students)
      return students
    },
  },
}
</script>

<style></style>
