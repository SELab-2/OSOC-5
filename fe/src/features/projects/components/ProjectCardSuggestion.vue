<template>
  <q-slide-transition :appear="!suggestion.reason">
    <div v-if="show" style="margin-left: 10px">
      <div class="column full-width">
        <div tabindex="-1" class="row">
          <q-item-section
            :lines="1"
            class="text-weight-medium"
            :class="removed ? 'text-strike' : ''"
          >
            {{ suggestion.student.firstName }}
            {{ suggestion.student.lastName }}
          </q-item-section>
          <div v-if="!removed">
            <btn tabindex="-1" class="gt-xs" size="sm" flat dense round icon="comment" />
            <btn tabindex="-1" class="gt-xs" size="sm" flat dense round icon="info" />
            <btn tabindex="-1"
              class="gt-xs"
              size="sm"
              flat
              dense
              round
              icon="delete"
              @click="() => {
                removed = true
                suggestion.reason === undefined ? remove() : prepareRemove()
              }"
            />
          </div>
          <btn v-else label="undo" @click="removed = false" />
        </div>
        <q-slide-transition v-if="progress >= 0">
          <q-input
            autofocus
            :color="suggestion.skill.color"
            v-if="undefined === suggestion.reason || progress !== 0"
            v-model="reason"
            dense
            outlined
            autogrow
            label="Comment"
          >
            <template v-slot:after>
              <btn
                :color="progress === 2 ? 'green' : suggestion.skill.color"
                dense
                flat
                :loading="progress === 1"
                @click="confirm"
                :icon="progress === 0 ? 'send' : 'check'"
                :glow-color="`${suggestion.skill.color}-2`"
              />
            </template>
          </q-input>
        </q-slide-transition>
        <div v-else class="row justify-evenly items-center text-red full-width">
          <q-icon size="20px" name="error" />
          <div>Cannot add suggestion.</div>
          <btn
            class="q-py-none"
            dense
            glow-color="red-2"
            label="retry"
            @click="() => {
              progress = 1
              confirm()
            }"
          />
        </div>
      </div>
    </div>
  </q-slide-transition>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { ProjectSuggestion } from '../../../models/ProjectSuggestion'
import { useProjectStore } from '../../../stores/useProjectStore'

export default defineComponent({
  props: {
    confirmSuggestion: {
      type: Function,
      required: true,
    },
    removeSuggestion: {
      type: Function,
      required: true,
    },
    suggestion: {
      type: ProjectSuggestion,
      required: true,
    },
  },
  data() {
    return {
      projectStore: useProjectStore(),
      show: ref(true),
      progress: ref(0),
      reason: ref(''),
      removed: ref(false),
    }
  },
  methods: {
    prepareRemove() {
      setTimeout(() => {
        if (!this.removed) return
        this.remove()
      }, 2000)
    },
    remove() {
      this.show = false
      setTimeout(() => {
        this.removeSuggestion(this.suggestion)
      }, 500)
      return
    },
    async confirm() {
      this.progress = 1
      this.suggestion.reason = this.reason
      try {
        await this.confirmSuggestion(this.suggestion)
        this.progress = 2
        setTimeout(() => (this.progress = 0), 500)
      } catch (error) {
        this.progress = -1
      }
    },
  },
})
</script>
