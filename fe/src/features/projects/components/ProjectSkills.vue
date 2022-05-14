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
      <NewSkillDialog
        v-model="showDialog"
        v-model:skill="editSkill"
      />

    <SkillTable :filter-skills="filterSkills" v-model:editSkill="editSkill" />
  </div>
</template>

<script lang="ts">
import {defineComponent} from "@vue/runtime-core";
import { ref } from "vue";
import SkillTable from "./subcomponents/SkillTable.vue";
import NewSkillDialog from "./subcomponents/NewSkillDialog.vue";
import { useSkillStore } from "../../../stores/useSkillStore";
import { Skill } from "../../../models/Skill"
export default defineComponent ({
  components: {NewSkillDialog, SkillTable},
  data() {
    let editSkill: Ref<Skill | null> = ref(null)
    return {
      skillStore: useSkillStore(),
      filterSkills: ref(''),
      newSkillPrompt: ref(false),
      editSkill,
      showDialog: ref(false)
    }
  },
  methods: {
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
      if (!newValue) {
        this.editSkill.id > 0 ? this.updateSkill() : this.addSkill()
      }
    },
    editSkill(newValue) {
      if (!this.showDialog) this.showDialog = true
    }
  }
})
</script>
