<template>
  <div class="variable">
    <div class="row">
      <div class="text-h4">
        Project Coaches
      </div>
      <q-space/>
      <q-input
        v-model="projectStore.filterCoaches"
        class="inputfield q-mb-sm"
        outlined
        dense
        debounce="300"
        color="green"
        placeholder="Search"
        @keydown.enter.prevent=""
      >
        <template #append>
          <q-icon
            v-if="projectStore.filterCoaches !== ''"
            name="close"
            class="cursor-pointer"
            @click="projectStore.filterCoaches = ''"
          />
          <q-icon
            v-if="projectStore.filterCoaches === ''"
            name="search"
          />
        </template>
      </q-input>
    </div>
    <div class="text-h6 row">
      <div>Selected Coaches</div>
      <q-space/>
      <div>Available Coaches</div>
    </div>
    <q-splitter
        v-model="splitterModel"
        style="height: 400px"
        :limits="[20,80]"
      >
      <template #before>
        
         
           <q-chip 
             v-for="coach in coaches"
             :key="coach.id"
             outline
             :color="getColorFromCoach(coach)"
             class="q-pr-none q-pl-sm"
             :class="`bg-${getColorFromCoach(coach)}-1`"
             style="border-width: 1.5px; width: fit-content;"
             @click="addCoachToProject(coach)"
           >
             <div class="row items-center">
               <span class="text-subtitle1 text-black">{{ coach.fullName }}</span>
               <btn
                 class="q-px-xs"
                 size="sm"
                 icon="o_delete"
                 @click="removeCoachFromProject(coach)"
               />
             </div>
             
           </q-chip>
           
         
      </template>
      <template #after>
        <div style="float: right; text-align: right">
          <q-chip 
            v-for="(coach,i) in coachStore.users"
            :key="coach.id"
            v-show="!coaches.some(c => c.id === coach.id)"
            outline
            clickable
            :color="getColor(i)"
            :class="`bg-${getColor(i)}-1`"
            style="border-width: 1.5px;"
            @click="addCoachToProject(coach)"
          >
            <div>
              <span class="text-subtitle1 text-black">{{ coach.fullName }}</span>
            </div>
            
          </q-chip>
        </div>
      </template>
    </q-splitter>
    
  </div>
</template>

<script lang="ts">
import {defineComponent, ref} from "vue";
import {useProjectStore} from "../../../stores/useProjectStore";
import {useCoachStore} from "../../../stores/useCoachStore";
import { User } from "../../../models/User"
import CoachTable from "./subcomponents/CoachTable.vue";
import CreateProjectChip from "./createprojectchip.vue"
import quasarColors from '../../../models/QuasarColors'

export default defineComponent({
  components: {CoachTable, CreateProjectChip},
  props: {
    coaches: {
      type: [Object] as PropType<User[]>,
      required: true
    }
  },
  setup() {
    const projectStore = useProjectStore()

    return {
      projectStore,
      quasarColors
    }
  },
  data() {
    return {
      coachStore: useCoachStore(),
      splitterModel: ref(50)
    }
  },
  methods: {
    addCoachToProject(coach: User) {
      this.coaches.push(coach)
    },
    removeCoachFromProject(coach: User) {
      const i = this.coaches.findIndex(s => s.id === coach.id)
      this.coaches.splice(i,1)
    },
    getColor(i: number) {
      return this.quasarColors[i%this.quasarColors.length]
    },
    getColorFromCoach(coach: User) {
      const i = this.coachStore.users.findIndex(c => c.id === coach.id)
      return this.getColor(i)
    }
  },
})
</script>

<style scoped>

@media only screen and (min-width: 1000px) {
  .variable {
    margin: auto;
    width: 70%
  }
}

</style>
