<template>
  <q-card
    class="my-card shadow-4 q-ma-sm"
    flat
    bordered
    :dark="$q.dark.isActive"
    style="border-radius: 10px !important"
  >
    <q-card-section>
      <div class="row no-wrap items-center">
        <h5
          class="text-bold q-mt-none q-mb-none"
          style="overflow: hidden; white-space: nowrap; text-overflow: ellipsis"
          :title="project.name"
        >
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
        <btn
          v-if="editable && me.isAdmin"
          flat
          round
          size="12px"
          color="teal"
          icon="edit"
          glow-color="teal-3"
          :to="`/projects/${project.id}`"
        />
        <btn
          round
          size="12px"
          glow-color="teal-3"
          shadow-color="teal"
          :shadow-strength="_showInfo ? 2 : 5"
          :color="_showInfo ? 'teal' : 'transparent'"
          :class="`text-${_showInfo ? 'white' : 'teal'}`"
          icon="info"
          @click="_showInfo = !_showInfo"
        />
      </div>

      <div class="text-overline">{{ project.partnerName }}</div>
      <q-slide-transition>
        <div v-if="_showInfo">
          <div class="text-h6">Info</div>
          <markdown-viewer
            style="overflow: hidden; overflow-wrap: break-word"
            v-model:text="project.extraInfo"
            :editable="me.isAdmin"
          ></markdown-viewer>
        </div>
      </q-slide-transition>
      <q-slide-transition>
        <div
          v-show="
            project.requiredSkills &&
            project.coaches &&
            project.suggestedStudents
          "
        >
          <div
            v-if="project.coaches && project.coaches.length > 0"
            class="text-caption text-grey"
          >
            Coaches:
          </div>
          <div v-else>There are no coaches assigned to this project.</div>
          <q-chip
            v-for="coach in project.coaches ?? []"
            :key="coach.id"
            icon="person"
          >
            {{ coach ? `${coach.firstName} ${coach.lastName
                                      .split(' ')
                                      .map((res) => res.charAt(0))
                                      .join('')}` : ''
            }}
          </q-chip>
          <div class="row" style="display: flex; align-items: center">
            <div
              v-if="(project.requiredSkills ?? []).length > 0"
              class="row flex-center"
            >
              <div class="text-caption text-grey">Skills:</div>
              <btn
                flat
                v-if="expandableSkills"
                round
                size="sm"
                @click="expanded = !expanded"
              >
                <q-icon
                  size="2em"
                  name="expand_more"
                  :class="expanded ? 'rotate180' : ''"
                  style="
                    transition: transform ease 500ms !important;
                    align-self: center;
                    justify-self: center;
                  "
                />
              </btn>
            </div>
            <div v-else>There are no skills assigned to this project.</div>
          </div>
          <div v-if="project.requiredSkills !== undefined">
            <project-role-chip
              v-show="project.requiredSkills"
              :modelValue="
                selectedRoles[skill.skill.id] || hovered === skill.skill.id
              "
              @update:modelValue="
                expandableSkills ? (selectedRoles[skill.skill.id] = $event) : ''
              "
              v-for="skill in project.requiredSkills"
              @dragleave="editable ? onDragLeave($event, skill) : false"
              @dragover="editable ? checkDrag($event, skill) : false"
              @drop="editable ? onDrop($event, skill) : false"
              :key="skill.skill.id"
              :skill="skill"
              :occupied="
                groupedStudents[skill.skill.id]?.length ??
                (editable || expandableSkills ? 0 : undefined)
              "
            />
          </div>
        </div>
      </q-slide-transition>

      <div
        class="column"
        v-for="(role, index) in project.requiredSkills ?? []"
        :key="index"
      >
        <q-slide-transition
          v-show="selectedRoles[role.skill.id] || hovered === role.skill.id"
        >
          <div class="text-bold" :class="'text-' + role.skill.color + '-8'">
            {{ role.skill.name }}
          </div>
        </q-slide-transition>

        <div v-for="suggestion in groupedStudents[role.skill.id] ?? []">
          <project-card-suggestion
            v-show="selectedRoles[role.skill.id] || hovered === role.skill.id || (suggestion as any).fromWebsocket || (suggestion as any).fromLocal"
            :confirmSuggestion="confirmSuggestion"
            :removeSuggestion="removeSuggestion"
            :suggestion="suggestion"
            :key="suggestion.student.id"
          />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>


<!-- A component for displaying a project. -->
<script lang="ts">
import ProjectRoleChip from './ProjectRoleChip.vue'
import { useProjectStore } from '../../../stores/useProjectStore'
import { ref, defineComponent } from 'vue'
import { useQuasar } from 'quasar'
import {
  ProjectSuggestionInterface,
  ProjectSuggestion,
  NewProjectSuggestion,
} from '../../../models/ProjectSuggestion'
import { ProjectSkillInterface } from '../../../models/Skill'
import { Project } from '../../../models/Project'
import { Student } from '../../../models/Student'
import { User } from '../../../models/User'
import { useAuthenticationStore } from '../../../stores/useAuthenticationStore'
import ProjectCardSuggestion from './ProjectCardSuggestion.vue'
import MarkdownViewer from './MarkdownViewer.vue'
export default defineComponent({
  props: {
    // The Project to display.
    project: {
      type: Project,
      required: true,
    },
    // If disabled, the edit button is hidden, expanding a skill is disabled, and a student cannot be dragged on a skill.
    editable: {
      type: Boolean,
      required: false,
    },
    expandableSkills: {
      type: Boolean,
      required: false
    },
    // This is used by other components to control the visibility of the extra info of a project.
    expandedInfo: {
      type: Boolean,
      required: false,
      default: undefined,
    },
  },
  components: { ProjectRoleChip, ProjectCardSuggestion, MarkdownViewer },
  setup() {
    return {
      authenticationStore: useAuthenticationStore(),
      q: useQuasar(),
      projectStore: useProjectStore(),
    }
  },
  data() {
    return {
      hovered: ref(-1),
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
    // Update a project whenever the extra info text is changed (by the markdown viewer).
    'project.extraInfo': {
      handler() {
        this.projectStore.updateProject(this.project, this.project.id)
      },
    },
  },

  methods: {
    async removeSuggestion(suggestion: ProjectSuggestionInterface) {
      try {
        // If the suggestion has not yet been posted to the server, don't make the POST call.
        // A suggestion has not yet been posted if it's an instance of NPS and the var fromLocal is enabled.
        if (
          !(
            suggestion instanceof NewProjectSuggestion &&
            (suggestion as NewProjectSuggestion)?.fromLocal
          )
        ) {
          // Remove from the server.
          await this.projectStore.removeSuggestion(this.project, suggestion)
        } else {
          // Only remove locally, this suggestion does not exist on the server yet.
          const index = this.project.suggestedStudents!.findIndex(
            (s) =>
              s.student.id === suggestion.student.id &&
              s.skill.id === suggestion.skill.id
          )
          this.project.suggestedStudents!.splice(index, 1)
        }
      } catch (error: any) {
        this.q.notify({
          icon: 'warning',
          color: 'warning',
          message: `Error ${error.response.status} while removing ${suggestion.student.firstName} ${suggestion.student.lastName} as ${suggestion.skill.name}`,
          textColor: 'black',
        })
      }
    },
    
    // Expand all the skills, so all the assigned students are visible.
    expand(skills: ProjectSkillInterface[]) {
      const indexes = skills.map((s) => s.skill.id)
      for (let i in this.selectedRoles) {
        this.selectedRoles[i] = indexes.includes(parseInt(i))
      }
    },

    // Calculates how many places of a role are occupied.
    amountLeft(skill: ProjectSkillInterface) {
      const occupied = this.groupedStudents[skill.skill.id]
      return skill.amount - (occupied ? occupied.length : 0)
    },

    // Check if a dragged student is already assigned to a skill.
    // If so, reject the drag.
    checkDrag(e: DragEvent, skill: ProjectSkillInterface) {
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
    onDragOver(e: DragEvent, skill: ProjectSkillInterface) {
      e.preventDefault()
      e.stopPropagation()
      this.hovered = skill.skill.id
      // this.selectedRoles[skill.skill.id] = true
    },

    // Hide the students assigned to a role when dragging away from the chip of that role.
    onDragLeave(e: DragEvent, skill: ProjectSkillInterface) {
      this.hovered = -1
    },

    // Assign a student to a role.
    async onDrop(e: DragEvent, skill: ProjectSkillInterface) {
      e.preventDefault()
      this.hovered = -1
      const target = <HTMLDivElement>e.target
      // don't drop on other draggables
      if (target.draggable === true) {
        return
      }
      
      // Try to parse the datatransfer.
      try {
        const data: { targetId: string; student: Student } = JSON.parse(
          e.dataTransfer!.getData(e.dataTransfer!.types[0])
        )
        this.selectedRoles[skill.skill.id] = true
        // Add a student to the project.
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
          new NewProjectSuggestion(
            {
              coach: this.me,
              reason: '',
              skill: skill.skill,
              student: data.student,
            },
            false
          )
        )

      } catch (error) {
        // When the data in the dragevent is not a valid format, the drag is rejected and nu further action is needed.
        return
      }
    },

    async confirmSuggestion(suggestion: NewProjectSuggestion) {
      // Downcast the suggestion from NewProjectSuggestion to ProjectSuggestion to convert the suggestion draft to a real suggestion.
      const i = this.project.suggestedStudents!.findIndex(
        (s) =>
          s.skill.id === suggestion.skill.id &&
          s.student.id === suggestion.student.id
      )
      setTimeout(
        () =>
          ((
            this.project.suggestedStudents![i] as NewProjectSuggestion
          ).fromLocal = false),
        500
      ) // This is needed, because JS will otherwise somehow report true, even when the object doesn't exist anymore? Don't know why.
      this.project.suggestedStudents![i] = new ProjectSuggestion(suggestion)

      await this.projectStore.addSuggestion(
        this.project.id,
        suggestion.student.url,
        suggestion.skill.url,
        suggestion.reason
      )
    },
  },
  computed: {
    me() {
      return this.authenticationStore.loggedInUser as User
    },
    expanded: {
      get() {
        const v = Object.values(this.selectedRoles)
        return v.every((r) => r) && v.length > 0
      },
      set(newValue: boolean) {
        for (let i in this.selectedRoles) {
          this.selectedRoles[i] = newValue
        }
      },
    },
    // Selectedroles is stored in the project itself instead of in the component state.
    // This is due to a bug with state in masonry-wall.
    selectedRoles: {
      get() {
        return (this.project as any).selectedRoles ?? {}
      },
      set(newValue: Record<number, boolean>) {
        ;(this.project as any).selectedRoles = newValue
      },
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
    _showInfo: {
      get(): boolean {
        return this.expandedInfo ?? (this.project as any).showInfo ?? false
      },
      set(n: boolean) {
        if (this.expandedInfo !== undefined) {
          this.$emit('update:expandedInfo', n)
        } else {
          (this.project as any).showInfo = n
        }
      },
    },
  },
})
</script>

<style>
.rotate180 {
  transform: rotate(180deg) !important;
}

.container {
  display: inline-block;
  width: max-content;
}
.second {
  max-width: fit-content;
}
</style>
