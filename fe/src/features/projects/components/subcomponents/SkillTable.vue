<template>
  <q-table
    class="table shadow-4"
    :rows="skillStore.skills"
    :columns="columnsSkills"
    :loading="skillStore.isLoadingSkills"
    row-key="skill"
    :filter="filterSkills"
    :filter-method="filterSkillsMethod"
  >
    <template #body="props">
      <q-tr
        :class="props.rowIndex % 2 === 1 ? 'bg-green-1' : ''"
        :props="props"
      >
        <q-td
          key="skill"
          :props="props"
          auto-width
        >
          {{ props.row.name }}
        </q-td>
        <q-td
          key="amount"
          :props="props"
          auto-width
        >
          {{ props.row.amount }}
          <q-popup-edit
            v-slot="scope"
            v-model.number="props.row.amount"
            buttons
            label-set="Save"
            label-cancel="Close"
            :validate="amountRangeValidation"
          >
            <q-input
              v-model.number="scope.value"
              type="number"
              hint="Enter a positive number."
              :error="errorSkillAmount"
              :error-message="errorMessageSkillAmount"
              dense
              autofocus
              borderless
              @keyup.enter="scope.set"
            />
          </q-popup-edit>
        </q-td>
        <q-td
          key="comment"
          :props="props"
        >
          <div v-if="props.row.comment.length !== 0">
            {{ props.row.comment }}
          </div>
          <div
            v-else
            style="font-style: italic; color: gray"
          >
            Click to add comment.
          </div>
          <q-popup-edit
            v-slot="scope"
            v-model="props.row.comment"
            buttons
          >
            <q-input
              v-model="scope.value"
              type="text"
              autogrow
              autofocus
              counter
              borderless
              @keyup.enter.stop
            />
          </q-popup-edit>
        </q-td>
        <q-td
          key="color"
          :props="props"
          auto-width
        >
          <q-chip
            :color="`${props.row.color}-8`"
            :class="`bg-${props.row.color}-4`"
            :style="`height: 25px; width:25px; border-radius: 50%`"
          />
        </q-td>
<!--        <q-td-->
<!--          key="edit"-->
<!--          style="width: 10px"-->
<!--        >-->
<!--          <btn-->
<!--            flat-->
<!--            round-->
<!--            style="color: #3d3d3d"-->
<!--            icon="mdi-pencil-outline"-->
<!--            glow-color="grey-5"-->
<!--            @click="editSkill(props.row)"-->
<!--          />-->
<!--        </q-td>-->
        <q-td
          key="remove"
          style="width: 10px"
        >
          <btn
            flat
            round
            style="color: #f14a3b"
            icon="mdi-trash-can-outline"
            glow-color="red-2"
            @click="deleteSkillMethod(props.row)"
          />
        </q-td>
      </q-tr>
    </template>
  </q-table>

  <q-dialog
    :model-value="editSkillDialog"
    class="full-width"
    persistent
  >
    <NewSkillDialog
      dialog-title="Edit skill"
    />
  </q-dialog>
  <q-dialog
    class="full-width"
    :model-value="deleteSkill !== -1"
    @update:model-value="deleteSkill = -1"
  >
    <DeleteSkillDialog
      :delete-skill-id="deleteSkill"
      :delete-skill-name="deleteSkillName"
    />
  </q-dialog>
</template>

<script lang="ts">
import { defineComponent } from '@vue/runtime-core'
import { ref } from 'vue'
import { ProjectTableSkill } from '../../../../models/Skill'
import { useSkillStore } from '../../../../stores/useSkillStore'
import columnsSkills from '../../../../models/ProjectSkillsColumns'
import DeleteSkillDialog from './DeleteSkillDialog.vue'

export default defineComponent({
  components: { DeleteSkillDialog },
  props: {
    filterSkills: {
      type: String,
      required: true,
    },
  },
  setup() {
    const skillStore = useSkillStore()

    const deleteSkill = ref(-1)
    const deleteSkillName = ref('')

    // Skill amount error handling
    const errorSkillAmount = ref(false)
    const errorMessageSkillAmount = ref('')

    // variables for the new skill dialog popup
    const editSkillDialog = ref(false)

    return {
      skillStore,
      deleteSkill,
      columnsSkills,
      errorSkillAmount,
      errorMessageSkillAmount,
      deleteSkillName,
      editSkillDialog,
    }
  },
  methods: {
    deleteSkillMethod(skill: ProjectTableSkill) {
      this.deleteSkill = skill.id
      this.deleteSkillName = skill.name
    },
    editSkill(skill: ProjectTableSkill) {
      this.editSkillDialog = true
      this.skillStore.popupID = skill.id
      this.skillStore.popupName = skill.name
      this.skillStore.popupColor = skill.color
    },
    amountRangeValidation(val: number) {
      if (val < 0) {
        this.errorSkillAmount = true
        this.errorMessageSkillAmount = 'The value must be positive!'
        return false
      }
      this.errorSkillAmount = false
      this.errorMessageSkillAmount = ''
      return true
    },
    filterSkillsMethod(){
      return this.skillStore.skills.filter(row => row.name.toLowerCase().startsWith(this.filterSkills))
    },
  }
})
</script>
<style scoped lang="sass">
thead tr:first-child th:first-child
//  /* bg color is important for th; just specify one */
//  background-color: #fff
//
//td:first-child
//  background-color: #f5f5dc
//
//th:first-child,
//td:first-child,
//th:second-child,
//  position: sticky
//  left: 0
//  z-index: 1
</style>