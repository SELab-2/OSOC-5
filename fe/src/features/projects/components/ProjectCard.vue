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
          <btn
            v-if="anyNew.length > 0"
            icon="r_warning"
            color="yellow"
            flat
            round
            size="12px"
            glow-color="amber-3"
            @click="expand(anyNew)"
            >
            <q-tooltip class="shadow-4 bg-amber-7">
            <div class="text-subtitle2">
              There are still draft suggestions open.
            </div>
          </q-tooltip>
          </btn>
          <btn flat round size="12px" color="primary" icon="mail" />
          <btn flat round size="12px" color="primary" icon="info" @click="showInfo = !showInfo"/>
          <btn flat round size="12px" color="primary" icon="edit" @click="triggerEditProject"/>
        </div>
      </div>

      <div class="text-overline">{{ project.partnerName }}</div>
      <q-slide-transition>
        <div v-if="showInfo">
        <div class="text-h6">Info</div>
        <div class="text-body2" >
        {{ project.extraInfo }}
        </div>
        <q-separator inset spaced="10px"/>
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
            <div v-if="(project.requiredSkills ?? []).length > 0" class="row flex-center">
              <div class="text-caption text-grey">Skills:</div>
              <btn

                flat
                round
                size="sm"
                @click="expanded = !expanded"
              >
              <q-icon
                size="2em"
                name="expand_more"
                :class="expanded ? 'rotate180' : ''"
                style="transition: transform ease 500ms !important; align-self: center; justify-self: center;"
                />
              </btn>
            </div>
            <div v-else>There are no skills assigned to this project.</div>

          </div>
          <div v-if="project.requiredSkills !== undefined">
            <project-role-chip
              v-show="project.requiredSkills"
              :modelValue="selectedRoles[skill.skill.id] || hovered === skill.skill.id"
              @update:modelValue="selectedRoles[skill.skill.id] = $event"
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
        <div v-show="selectedRoles[role.skill.id] || hovered === role.skill.id">
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
        </div>
      </q-slide-transition>
    </q-card-section>
  </q-card>
</template>

<script lang="ts">
import ProjectRoleChip from './ProjectRoleChip.vue'
import { useProjectStore } from '../../../stores/useProjectStore'
import { ref, defineComponent } from 'vue'
import { useQuasar } from 'quasar'
import {
  ProjectSuggestionInterface,
  ProjectSuggestion,
  NewProjectSuggestion
} from '../../../models/ProjectSuggestion'
import { ProjectSkillInterface } from '../../../models/Skill'
import { Project } from '../../../models/Project'
import { Student } from '../../../models/Student'
import { User } from '../../../models/User'
import { useAuthenticationStore } from '../../../stores/useAuthenticationStore'
import ProjectCardSuggestion from './ProjectCardSuggestion.vue'
import router from "../../../router";


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
    return {
      hovered: ref(-1),
      showInfo: ref(false)
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

    async removeSuggestion(suggestion: ProjectSuggestion) {
      try {
        // If the suggestion has not yet been posted to the server, don't make the POST call.
        if (!(suggestion instanceof NewProjectSuggestion)) {
          await this.projectStore.removeSuggestion(this.project, suggestion)
        } else {
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
    expand(skills: ProjectSkillInterface[]) {
      const indexes = skills.map(s => s.skill.id);
      for (let i in this.selectedRoles) {
        this.selectedRoles[i] = indexes.includes(parseInt(i))
      }
    },

    // Calculates how many places of a role are occupied.
    amountLeft(skill: ProjectSkillInterface) {
      const occupied = this.groupedStudents[skill.skill.id]
      return skill.amount - (occupied ? occupied.length : 0)
    },

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
      this.selectedRoles[skill.skill.id] = true
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
        new NewProjectSuggestion({
          coach: this.me,
          reason: '',
          skill: skill.skill,
          student: data.student,
        })
      )

      // Hide the expanded list after dragging. If the list was already expanded by the user, don't hide it.
      if (!this.expanded) {
        // setTimeout(() => (this.selectedRoles[skill.skill.id] = false), 1000)
      }
    },
    async confirmSuggestion(suggestion: NewProjectSuggestion) {
      // Downcast the suggestion from NewProjectSuggestion to ProjectSuggestion to convert the suggestion draft to a real suggestion.
      const i = this.project.suggestedStudents!.findIndex(s => s.skill.id === suggestion.skill.id && s.student.id === suggestion.student.id)
      this.project.suggestedStudents![i] = new ProjectSuggestion(suggestion)

      await this.projectStore.addSuggestion(
        this.project.id,
        suggestion.student.url,
        suggestion.skill.url,
        suggestion.reason
      )
    },
    triggerEditProject(){
      router.push('/projects/' + this.project.id)
    }

  },
  computed: {
    anyNew() {
      return (this.project.requiredSkills ?? []).filter(s => {
        return !this.selectedRoles[s.skill.id] && (this.project.suggestedStudents ?? []).filter(student => student.skill.id === s.skill.id).some(student => student instanceof NewProjectSuggestion)
      })
      // return this.project.suggestedStudents?.some(s => s instanceof NewProjectSuggestion )
    },
    me() {
      return this.authenticationStore.loggedInUser as User
    },
    expanded: {
      get() {
        const v = Object.values(this.selectedRoles)
        return v.every(r => r) && v.length > 0
      },
      set(newValue: boolean) {
        for (let i in this.selectedRoles) {
          this.selectedRoles[i] = newValue
        }
      }
    },
    // Selectedroles is stored in the project itself instead of in the component state.
    // This is due to a bug with state in masonry-wall.
    selectedRoles: {
      get() {
        return (this.project as any).selectedRoles ?? {}
      },
      set(newValue: Record<number,boolean>) {
        (this.project as any).selectedRoles = newValue
      }
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

<style>

.rotate180 {
  transform: rotate( 180deg ) !important;
}
</style>
