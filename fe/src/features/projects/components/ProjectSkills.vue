<template>
    <div style="overflow: hidden" class="fit column">
    <div class="row">
      <div class="text-h4">
        Project Skills
      </div>
      <q-space/>
        <btn
          round
          style="margin-bottom: 15px"
          size="12px"
          glow-color="teal-3"
          shadow-color="teal"
          :shadow-strength="2"
          color="teal"
          class="text-white"
          icon="add"
          @click="showDialog = true"
        />
        <btn
          round
          style="margin-bottom: 15px"
          size="12px"
          glow-color="teal-3"
          shadow-color="teal"
          :shadow-strength="editMode ? 2 : 5"
          :color="editMode ? 'teal' : 'white'"
          :class="`text-${editMode ? 'white' : 'teal'}`"
          icon="mdi-pencil-outline"
          @click="editMode = !editMode"
        />
      <q-input
        v-model="filterSkills"
        style="max-width: 190px"
        outlined
        dense
        debounce="300"
        color="green"
        class="inputfield q-mb-sm"
        placeholder="Search"
        @keydown.enter.prevent=""
      >
        <template #append>
          <q-icon
            v-if="filterSkills !== ''"
            name="close"
            class="cursor-pointer"
            @click="filterSkills = ''"
          />
          <q-icon
            v-if="filterSkills === ''"
            name="search"
          />
        </template>
      </q-input>
    </div>
    <div class="row text-h6">
      <div>Selected Skills</div>
      <q-space/>
      <div>Available Skills</div>
    </div>
    <q-splitter
      v-model="splitterModel"
      style="flex: 1; overflow: auto"
      :limits="[20,80]"
    >
    <template #before>
      
       
         <div v-if="skills.length === 0" class="placeholder">
           <div class="q-mb-xl">
               <lottie-animation animationLink="https://assets8.lottiefiles.com/packages/lf20_av8ts5jt.json" :height="200" :width="200" style="transform: rotate(180deg)" />
               <h6 class="text-bold q-mt-none q-mb-xl">Select a skill to add it to the project.</h6>
           </div>
         </div>
         <div v-else>
         <create-project-chip
         v-for="skill in skills"
          :key="skill.skill.id"
          :skill="skill"
          @remove="removeSkillFromProject(skill.skill)"
          />
         </div>
         
       
    </template>
    <template #after>
      <div style="float: right; text-align: right">
        <q-chip 
          v-for="skill in skillStore.skills"
          :key="skill.id"
          v-show="!skills.some(s => s.skill.id === skill.id)"
          outline
          clickable
          :color="`${skill.color}-4`"
          :class="`bg-${skill.color}-1`"
          style="border-width: 1.5px; width: fit-content;"
          @click="() => { if (editMode) { editSkill = skill; showDialog = true} else { addSkillToProject(skill) }}"
        >
          <div>
            <span class="text-subtitle1 text-black">{{ skill.name }}</span>
          </div>
          
        </q-chip>
      </div>
    </template>
  </q-splitter>
    
      <NewSkillDialog
        v-model="showDialog"
        v-model:skill="editSkill"
      />
    </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref, PropType } from "vue";
import NewSkillDialog from "./subcomponents/NewSkillDialog.vue";
import { useSkillStore } from "../../../stores/useSkillStore";
import { Skill, ProjectSkill } from "../../../models/Skill"
import ProjectRoleChip from "./ProjectRoleChip"
import CreateProjectChip from "./createprojectchip.vue"
import LottieAnimation from '../../../components/LottieAnimation.vue'

export default defineComponent ({
  components: {NewSkillDialog, CreateProjectChip, LottieAnimation},
  props: {
    skills: {
      type: [Object] as PropType<ProjectSkill[]>,
      required: true
    }
  },
  data() {
    let editSkill: Ref<Skill | null> = ref(null)
    return {
      skillStore: useSkillStore(),
      filterSkills: ref(''),
      newSkillPrompt: ref(false),
      editSkill,
      showDialog: ref(false),
      editMode: ref(false),
      splitterModel: ref(70)
    }
  },
  methods: {
    addSkillToProject(skill: Skill) {
      this.skills.push(new ProjectSkill(1, '', skill))
    },
    removeSkillFromProject(skill: Skill) {
      const i = this.skills.findIndex(s => s.skill.id === skill.id)
      console.log(i)
      this.skills.splice(i,1)
    },
    addSkill() {
      this.skillStore.addSkill(this.editSkill, (success: boolean) => {
        this.$q.notify({
          icon: success ? 'done' : 'close',
          color: success ? 'positive' : 'negative',
          message: success ? 'Success' : 'Failed'
        })
      })
    },
    updateSkill() {
      this.skillStore.updateSkill(this.editSkill, () => {
        this.$q.notify({
          icon: 'close',
          color: 'negative',
          message: 'Failed to update'
        })
      })
    }
  },
  watch: {
    showDialog(newValue) {
      // newValue false means the popup closed
      if (!newValue && this.editSkill) {
        this.editSkill.id > 0 ? this.updateSkill() : this.addSkill()
      }
    },
  },
})
</script>
