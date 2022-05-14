<template>
  <div
    class="projectcol col-xs-12 col-sm-12 col-md-12 col-lg-12 col-xl-6"
  >
    <div class="text-h4 q-my-md">
      Project Skills
    </div>
    <div class="row">
      <btn
        class="cornered q-mb-sm"
        color="primary"
        icon="add"
        label="Add skill"
        shadow-strength="2"
        glow-color="#00F1AF"
        @click="showDialog = true"
      />
      
      <q-space />
        <btn
          size="sm"
          color="primary"
          icon="mdi-pencil-outline"
          shadow-strength="2"
          glow-color="#00F1AF"
          @click="showEditIcons = !showEditIcons"
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
    
    <div class="row no-wrap justify-between">
     <div style="width: 40%; float:left">
       <div class="text-h6">Selected Skills</div>
       <create-project-chip
       v-for="skill in projectSkills"
        :key="skill.skill.id"
        :skill="skill"
        />
       
     </div>
     <q-splitter/>
    <div style="width: 40%; float: right; text-align: right">
      <div class="text-h6">Available Skills</div>
      <q-chip 
        v-for="skill in skillStore.skills"
        :key="skill.id"
        v-show="!projectSkills.some(s => s.skill.id === skill.id)"
        outline
        clickable
        :color="`${skill.color}-4`"
        :class="`bg-${skill.color}-1`"
        style="border-width: 1.5px;"
        @click="addSkillToProject(skill)"
      >
        <div>
          <span class="text-subtitle1 text-black">{{ skill.name }}</span>
          <btn
            v-if="showEditIcons"
            flat
            round
            style="color: #3d3d3d"
            icon="mdi-pencil-outline"
            glow-color="grey-5"
            @click="editSkill = skill; showDialog=true"
          />
        </div>
        
      </q-chip>
    </div>
    </div>
    
      <NewSkillDialog
        v-model="showDialog"
        v-model:skill="editSkill"
      />

    <SkillTable :filter-skills="filterSkills" v-model:editSkill="editSkill" v-model:showDialog="showDialog" />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import SkillTable from "./subcomponents/SkillTable.vue";
import NewSkillDialog from "./subcomponents/NewSkillDialog.vue";
import { useSkillStore } from "../../../stores/useSkillStore";
import { Skill, ProjectSkill } from "../../../models/Skill"
import ProjectRoleChip from "./ProjectRoleChip"
import CreateProjectChip from "./createprojectchip.vue"
export default defineComponent ({
  components: {NewSkillDialog, SkillTable,CreateProjectChip},
  data() {
    let editSkill: Ref<Skill | null> = ref(null)
    return {
      skillStore: useSkillStore(),
      filterSkills: ref(''),
      newSkillPrompt: ref(false),
      editSkill,
      showDialog: ref(false),
      projectSkills: ref([]),
      showEditIcons: ref(false)
    }
  },
  methods: {
    addSkillToProject(skill: Skill) {
      this.projectSkills.push(new ProjectSkill(0, '', skill))
    },
    removeSkillFromProject(skill: Skill) {
      const i = this.projectSkills.findIndex(s => s.skill.id === skill.id)
      this.projectSkills.slice(i,1)
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
  computed: {
    selectedSkills: {
      get() {
        return this.projectSkills.map(s => s.skill)
      },
      set(n) {
        console.log(n)
        const oldSkills = this.projectSkills.map(s => s.skill)
        n.filter(s => !oldSkills.includes(s)).forEach(s => {
          this.projectSkills.push(new ProjectSkill(0, '', s))
        })
      }
    }
  }
})
</script>
