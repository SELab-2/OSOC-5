<template>
  <q-table
    class="table shadow-4"
    :rows="skillStore.skills"
    :columns="columnsSkills"
    :loading="skillStore.isLoadingSkills"
    row-key="name"
    :filter="filterSkills"
  >
    <template #body="props">
      <q-tr
        :class="props.rowIndex % 2 === 1 ? 'bg-green-1' : ''"
        :props="props"
      >
        <q-td key="skill" :props="props">
          {{ props.row.name }}
        </q-td>
        <q-td key="amount" :props="props">
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
        <q-td key="comment" :props="props">
          <div>{{ props.row.comment }}</div>
          <q-popup-edit v-slot="scope" v-model="props.row.comment" buttons>
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
        <q-td key="color" :props="props" auto-width>
          <div
            :style="`height: 25px; width:25px; border-radius: 50%;background: ${props.row.color}`"
          />
          <!--          &lt;!&ndash; TODO make this actually change in the database not locally&ndash;&gt;-->
          <!--          <q-popup-edit-->
          <!--            v-slot="scope"-->
          <!--            v-model="props.row.color"-->
          <!--            buttons-->
          <!--          >-->
          <!--            <q-color-->
          <!--              v-model="scope.value"-->
          <!--              no-header-->
          <!--              no-footer-->
          <!--              class="color-picker"-->
          <!--              @keyup.enter.stop-->
          <!--            />-->
          <!--          </q-popup-edit>-->
        </q-td>
        <q-td key="remove" style="width: 10px">
          <btn
            flat
            round
            style="color: #f14a3b"
            icon="mdi-trash-can-outline"
            glow-color="red-2"
            @click="delete_skill(props.row)"
          />
        </q-td>
      </q-tr>
    </template>
  </q-table>

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
import columnsSkills from '../../../../models/ProjectRolesColumns'
import DeleteSkillDialog from './DeleteSkillDialog.vue'

export default defineComponent({
  components: { DeleteSkillDialog },
  setup() {
    const skillStore = useSkillStore()

    // Filters
    const filterSkills = ref('')

    const deleteSkill = ref(-1)
    const deleteSkillName = ref('')

    // Skill amount error handling
    const errorSkillAmount = ref(false)
    const errorMessageSkillAmount = ref('')

    return {
      skillStore,
      deleteSkill,
      filterSkills,
      columnsSkills,
      errorSkillAmount,
      errorMessageSkillAmount,
      deleteSkillName,
    }
  },
  methods: {
    delete_skill(skill: ProjectTableSkill) {
      this.deleteSkill = skill.id
      this.deleteSkillName = skill.name
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
  },
})
</script>
