<template>
  <q-card class="my-card shadow-4 q-ma-sm" flat bordered>
    <q-card-section>
      <div class="row">
        <h5 class="text-bold q-mt-none q-mb-none">
          {{ project.name }}
        </h5>
        <q-spinner
          v-show="
            !(
              project.requiredSkills &&
              project.coaches &&
              project.suggestedStudents
            )
          "
          size="20px"
          color="primary"
          class="q-ml-sm q-mt-xs"
        />
        <q-space />
        <div>
          <btn flat round size="12px" color="primary" icon="mail" />
          <btn flat round size="12px" color="primary" icon="info" />
          <btn flat round size="12px" color="primary" icon="edit" />
        </div>
      </div>

      <div class="text-overline">{{ project.partnerName }}</div>
      <q-slide-transition>
        <div
          v-show="
            project.requiredSkills &&
            project.coaches &&
            project.suggestedStudents
          "
        >
          <div class="text-caption text-grey">Coaches:</div>
          <q-chip
            v-for="coach in project.coaches ?? []"
            :key="coach.id"
            icon="person"
          >
            {{ coach.firstName }}
            {{
              coach.lastName
                .split(' ')
                .map((res) => res.charAt(0))
                .join('')
            }}.
          </q-chip>
          <div class="row" style="display: flex; align-items: center">
            <div class="text-caption text-grey">Roles:</div>
            <q-btn
              flat
              round
              size="sm"
              icon="mdi-eye"
              @click="
                () => {
                  expanded = !expanded
                  toggleExpanded(expanded)
                }
              "
            />
          </div>

          <div v-if="project.requiredSkills !== undefined">
            <project-role-chip
              v-show="project.requiredSkills"
              v-model="selectedRoles[skill.skill.id]"
              v-for="(skill, index) in project.requiredSkills"
              @dragleave="onDragLeave($event, skill)"
              @dragover="checkDrag($event, skill)"
              @drop="onDrop($event, skill)"
              :key="index"
              :skill="skill"
              :occupied="groupedStudents[skill.skill.id]?.length"
            />
          </div>
        </div>
      </q-slide-transition>

      <q-slide-transition
        v-for="(role, index) in project.requiredSkills ?? []"
        :key="index"
      >
        <div v-show="selectedRoles[role.skill.id]">
          <q-item-label
            class="text-subtitle1 text-bold"
            :class="'text-' + role.skill.color + '-8'"
          >
            {{ role.skill.name }}
          </q-item-label>
          <q-slide-transition
            :appear="!suggestion.coach"
            v-for="suggestion in groupedStudents[role.skill.id] ?? []"
            :key="suggestion.student.id"
          >
            <div v-if="suggestion.student.email" style="margin-left: 10px">
              <div class="column full-width">
                <div class="row">
                  <q-item-section :lines="1" class="text-weight-medium">
                    {{ suggestion.student.firstName }}
                    {{ suggestion.student.lastName }}
                  </q-item-section>
                  <btn
                    class="gt-xs"
                    size="sm"
                    flat
                    dense
                    round
                    icon="comment"
                  />
                  <btn class="gt-xs" size="sm" flat dense round icon="info" />
                  <btn
                    class="gt-xs"
                    size="sm"
                    flat
                    dense
                    round
                    icon="delete"
                    @click="removeSuggestion(suggestion)"
                  />
                </div>
                <q-slide-transition>
                  <q-input
                    :color="role.skill.color"
                    v-if="suggestion.coach === undefined"
                    v-model="suggestion.reason"
                    dense
                    outlined
                    autogrow
                    label="Comment"
                  >
                    <template v-slot:after>
                      <q-btn
                        :color="role.skill.color"
                        round
                        dense
                        flat
                        @click="confirmSuggestion(suggestion)"
                        :icon="loading ? 'check' : 'send'"
                      />
                    </template>
                  </q-input>
                </q-slide-transition>
              </div>
            </div>
          </q-slide-transition>
        </div>
      </q-slide-transition>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import ProjectRoleChip from './ProjectRoleChip.vue'
import { useProjectStore } from '../../../stores/useProjectStore'
import { reactive, ref, Ref, nextTick, defineComponent } from 'vue'
import { useQuasar } from 'quasar'
import { ProjectSuggestion } from '../../../models/ProjectSuggestion'
import { ProjectSkillInterface, Skill } from '../../../models/Skill'
import { Project } from '../../../models/Project'
import { Student } from '../../../models/Student'
import { User } from '../../../models/User'
import { useAuthenticationStore } from '../../../stores/useAuthenticationStore'
var test = 0
export default defineComponent({
  props: {
    project: {
      type: Project,
      required: true,
    },
  },
  components: { ProjectRoleChip },
  setup() {
    return {
      authenticationStore: useAuthenticationStore(),
      q: useQuasar(),
      projectStore: useProjectStore(),
    }
  },

  data() {
    const selectedRoles: Record<number, boolean> = reactive({})
    return {
      expanded: ref(false),
      selectedRoles,
      loading: ref(false),
    }
  },
  watch: {
    // The skills are fetched later on, thus the list needs to be updated manually.
    'project.requiredSkills': {
      handler(newVal: ProjectSkillInterface[]) {
        this.selectedRoles =
          newVal.length === 0
            ? {}
            : newVal.reduce(
                (obj: any, skill) => ((obj[skill.skill.id] = false), obj),
                {}
              )
      },
    },
  },

  methods: {
    // Expand/Hide the whole student list.
    toggleExpanded(state: boolean) {
      Object.keys(this.selectedRoles).forEach((key) => {
        this.selectedRoles[key as any as number] = state
      })
    },

    async removeSuggestion(suggestion: ProjectSuggestion) {
      const suggest = { ...suggestion }
      suggestion.student.email = undefined
      
      await setTimeout(async () => {
        try {
          await this.projectStore.removeSuggestion(this.project, suggest)
          const index = this.project.suggestedStudents!.findIndex(
            (s) =>
              s.student.id === suggestion.student.id &&
              s.skill.id === suggestion.skill.id
          )
          this.project.suggestedStudents!.splice(index, 1)
        } catch (error) {
          this.q.notify({
            icon: 'warning',
            color: 'warning',
            message: `Error ${error.response.status} while removing ${suggest.student.firstName} ${suggest.student.lastName} as ${suggest.skill.name}`,
            textColor: 'black',
          })
          suggestion.student = suggest.student
        }
      }, 2000)
    },

    // Calculates how many places of a role are occupied.
    amountLeft(skill: ProjectSkillInterface) {
      const occupied = this.groupedStudents[skill.skill.id]
      return skill.amount - (occupied ? occupied.length : 0)
    },

    checkDrag(e: MouseEvent, skill: ProjectSkillInterface) {
      const data: { targetId: string; student: Student } = JSON.parse(
        e.dataTransfer!.getData('text')
      )
      if (
        this.groupedStudents?.[skill.skill.id]?.some(
          (suggestion) => suggestion.student.id === data.student.id
        )
      )
        return ''
      return this.amountLeft(skill) > 0 ? this.onDragOver(e, skill) : ''
    },

    // Show the students assigned to a role when dragging over the chip of that role.
    onDragOver(e: MouseEvent, skill: ProjectSkillInterface) {
      e.preventDefault()
      e.stopPropagation()
      this.selectedRoles[skill.skill.id] = true
    },

    // Hide the students assigned to a role when dragging away from the chip of that role.
    onDragLeave(e: MouseEvent, skill: ProjectSkillInterface) {
      if (!this.expanded) {
        this.selectedRoles[skill.skill.id] = false
      }
    },

    // Assign a student to a role.
    async onDrop(e: DragEvent, skill: ProjectSkillInterface) {
      e.preventDefault()
      const target = <HTMLDivElement>e.target
      // don't drop on other draggables
      if ((<HTMLDivElement>e.target).draggable === true) {
        return
      }
      // TODO: additional checks that datatransfer is valid and not null
      const data: { targetId: string; student: Student } = JSON.parse(
        e.dataTransfer!.getData('text')
      )

      // Add a student to the project.
      const reason = 'mimimi'
      let coach = this.authenticationStore.loggedInUser as User
      if (!coach) {
        this.q.notify({
          icon: 'warning',
          color: 'warning',
          message: 'You are not logged in.',
          textColor: 'black',
        })
        return
      }

      this.project.suggestedStudents?.push({
        coach: undefined,
        reason: '',
        skill: skill.skill,
        student: data.student,
      })

      // Hide the expanded list after dragging. If the list was already expanded by the user, don't hide it.
      if (!this.expanded) {
        // setTimeout(() => (this.selectedRoles[skill.skill.id] = false), 1000)
      }
    },
    async confirmSuggestion(suggestion) {
      this.loading = true
      await this.projectStore.addSuggestion(
        this.project.id,
        suggestion.student.url,
        suggestion.skill.url,
        suggestion.reason
      )
      setTimeout(() => {
        suggestion.coach = this.me
        this.loading = false
      }, 800)
    },
  },
  computed: {
    me() {
      return this.authenticationStore.loggedInUser as User
    },
    // Groups the students by role.
    // Example: { 'backend' : [{student1}, {student2}] }
    groupedStudents(): Record<string, ProjectSuggestion[]> {
      if (!this.project.suggestedStudents) return {}
      return this.project.suggestedStudents.reduce((obj: any, student) => {
        if (!obj[student.skill.id]) {
          obj[student.skill.id] = []
        }
        obj[student.skill.id].push(student)
        return obj
      }, {})
    },
  },
})
</script>
