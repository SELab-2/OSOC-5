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
          <project-card-suggestion
            :confirmSuggestion="confirmSuggestion"
            :removeSuggestion="removeSuggestion"
            :suggestion="suggestion"
            v-for="suggestion in groupedStudents[role.skill.id] ?? []"
            :key="suggestion.student.id"
          />
          <!-- <q-slide-transition
            :appear="!suggestion.coach"
            v-for="suggestion in groupedStudents[role.skill.id] ?? []"
            :key="suggestion.student.id"
          >
            
          </q-slide-transition> -->
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
import {
  ProjectSuggestionInterface,
  ProjectSuggestion,
} from '../../../models/ProjectSuggestion'
import { ProjectSkillInterface, Skill } from '../../../models/Skill'
import { Project } from '../../../models/Project'
import { Student } from '../../../models/Student'
import { User } from '../../../models/User'
import { useAuthenticationStore } from '../../../stores/useAuthenticationStore'
import ProjectCardSuggestion from './ProjectCardSuggestion.vue'
import { Suggestion } from '../../../models/Suggestion'
var test = 0
export default defineComponent({
  props: {
    project: {
      type: Project,
      required: true,
    },
  },
  components: { ProjectRoleChip, ProjectCardSuggestion },
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

    async removeSuggestion(suggestion: ProjectSuggestionInterface) {
      try {
        // If the suggestion has not yet been posted to the server, don't make the POST call.
        if (suggestion.reason !== undefined) {
          await this.projectStore.removeSuggestion(this.project, suggestion)
        }
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
          message: `Error ${error.response.status} while removing ${suggestion.student.firstName} ${suggestion.student.lastName} as ${suggestion.skill.name}`,
          textColor: 'black',
        })
      }
    },

    // Calculates how many places of a role are occupied.
    amountLeft(skill: ProjectSkillInterface) {
      const occupied = this.groupedStudents[skill.skill.id]
      return skill.amount - (occupied ? occupied.length : 0)
    },

    checkDrag(e: MouseEvent, skill: ProjectSkillInterface) {
      const id: number = parseInt(e.dataTransfer!.types[0])
      if (
        this.groupedStudents?.[skill.skill.id]?.some(
          (suggestion) => suggestion.student.id === id
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
        e.dataTransfer!.getData(e.dataTransfer!.types[0])
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
      this.project.suggestedStudents?.push(
        new ProjectSuggestion({
          coach: this.me,
          reason: undefined,
          skill: skill.skill,
          student: data.student,
        })
      )

      // Hide the expanded list after dragging. If the list was already expanded by the user, don't hide it.
      if (!this.expanded) {
        // setTimeout(() => (this.selectedRoles[skill.skill.id] = false), 1000)
      }
    },
    async confirmSuggestion(suggestion: ProjectSuggestion) {
      this.loading = true
      await this.projectStore.addSuggestion(
        this.project.id,
        suggestion.student.url,
        suggestion.skill.url,
        suggestion.reason
      )
    }
    
  },
  computed: {
    me() {
      return this.authenticationStore.loggedInUser as User
    },
    // Groups the students by role.
    // Example: { 'backend' : [{student1}, {student2}] }
    groupedStudents(): Record<string, ProjectSuggestionInterface[]> {
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
