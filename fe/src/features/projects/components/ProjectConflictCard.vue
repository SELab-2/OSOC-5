<template>
  <q-card
    class="my-card shadow-4 q-ma-sm"
    flat
    bordered
  >
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
      </div>

      <div class="text-overline">
        {{ project.partnerName }}
      </div>
      <q-slide-transition>
        <div v-if="showInfo">
          <div class="text-h6">
            Info
          </div>
          <div class="text-body2">
            {{ project.extraInfo }}
          </div>
          <q-separator
            inset
            spaced="10px"
          />
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
          <div class="text-caption text-grey">
            Coaches:
          </div>
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
          <div
            class="row"
            style="display: flex; align-items: center"
          >
            <div
              v-if="(project.requiredSkills ?? []).length > 0"
              class="row flex-center"
            >
              <div class="text-caption text-grey">
                Skills:
              </div>
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
            <div v-else>
              There are no skills assigned to this project.
            </div>
          </div>
          <div v-if="project.requiredSkills !== undefined">
            <project-role-chip
              v-for="(skill, index) in project.requiredSkills"
              v-show="project.requiredSkills"
              :key="index"
              :model-value="selectedRoles[skill.skill.id] || hovered === skill.skill.id"
              :skill="skill"
              :occupied="groupedStudents[skill.skill.id]?.length"
              @update:modelValue="selectedRoles[skill.skill.id] = $event"
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
            v-for="suggestion in groupedStudents[role.skill.id] ?? []"
            :key="suggestion.student.id"
            :suggestion="suggestion"
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
  NewProjectSuggestion
} from '../../../models/ProjectSuggestion'
import { ProjectSkillInterface } from '../../../models/Skill'
import { Project } from '../../../models/Project'
import { User } from '../../../models/User'
import { useAuthenticationStore } from '../../../stores/useAuthenticationStore'
import ProjectCardSuggestion from './ProjectCardSuggestion.vue'

export default defineComponent({
  components: { ProjectRoleChip, ProjectCardSuggestion },
  props: {
    project: {
      type: Project,
      required: true,
    },
  },
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
  },
})
</script>

<style>

.rotate180 {
  transform: rotate( 180deg ) !important;
}
</style>
