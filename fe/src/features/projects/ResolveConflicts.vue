<template>
  <div
    class="q-pa-md"
    style="max-width: 350px"
  >
    <q-list
      bordered
      separator
    >
      <q-item
        v-for="conflict in conflicts"
        :key="conflict.user"
        v-ripple
        clickable
      >
        <q-item-section>{{ fullname(conflict.user) }}</q-item-section>
      </q-item>
    </q-list>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue'
import { useProjectStore } from '../../stores/useProjectStore'

export default defineComponent({
    async setup() {
        const projectStore = useProjectStore()
        const conflicts = await projectStore.getConflictingProjects()

        return {
            projectStore,
            conflicts
        }
    },
    methods: {
      fullName(user: { firstName: string; lastName: string }) {
        return `${user.firstName} ${user.lastName}`
      }
    }
})
</script>
