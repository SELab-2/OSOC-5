<template>
  <q-slide-transition :appear="isNew && !suggestion.reason">
    <div v-if="show" style="margin-left: 10px">
      <div class="column full-width" style="justify-content: center">
        <div :lines="1" tabindex="-1" class="row" style="height: 30px; flex-wrap: nowrap;">
          <div
            class="text-weight-medium row"
            :class="removed ? 'text-strike' : ''"
            style="white-space: nowrap;overflow: hidden;display: block;text-overflow: ellipsis; margin-top: 3px;"
          >
          
            {{ suggestion.student.firstName }}
            {{ suggestion.student.lastName }}
          </div>
          <q-badge v-if="isNew" rounded :color="suggestion.skill.color" label="Draft" class="q-ml-xs" style="height: 15px; margin-top: 6px" />
          
          <q-space/>
          <div v-if="!removed" style="flex-wrap: nowrap; display: block; min-width: 72px">
            <btn tabindex="-1" class="gt-xs" size="sm" @mouseover="() => {
              if (progress === 0) progress = 3
            }" @mouseleave="() => {
              if (progress === 3) progress = 0
            }" flat dense round icon="r_comment" />
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
                isNew ? remove() : prepareRemove()
              }"
            />
          </div>
          <btn v-else label="undo" @click="stop" dense style="justify-content: center; height: 30px"/>
        </div>
        <q-slide-transition v-if="progress >= 0">
          <q-input
            :autofocus="progress !== 3"
            :color="suggestion.skill.color"
            v-if="isNew || progress !== 0"
            v-model="suggestion.reason"
            dense
            outlined
            autogrow
            label="Comment (Optional)"
            :disabled="progress === 3"
          >
            <template v-slot:after v-if="progress !== 3">
              <btn
                :color="progress === 2 ? 'positive' : suggestion.skill.color"
                dense
                flat
                focusable
                padding="sm"
                :loading="progress === 1"
                @click="confirm"
                :icon="progress === 0 ? 'r_send' : 'r_check'"
                :glow-color="progress === 2 ? 'green-2' : `${suggestion.skill.color}-2`"
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
import { ProjectSuggestion, NewProjectSuggestion } from '../../../models/ProjectSuggestion'
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
    let timeout: any | null = null
    return {
      projectStore: useProjectStore(),
      show: ref(true),
      progress: ref(0),
      removed: ref(false),
      timeout
    }
  },
  beforeUnmount() {
    if (this.timeout) {
      clearTimeout(this.timeout)
      this.remove()
    }
  },
  methods: {
    stop() {
      this.removed = false
      if (!this.timeout) return
      clearTimeout(this.timeout)
      this.timeout = null
    },
    prepareRemove() {
      this.timeout = setTimeout(() => {
        this.remove()
        this.timeout = null
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
      try {
        await this.confirmSuggestion(this.suggestion)
        this.progress = 2
        setTimeout(() => (this.progress = 0), 500)
      } catch (error) {
        this.progress = -1
      }
    },
  },
  computed: {
    isNew() {
      return this.suggestion instanceof NewProjectSuggestion
    }
  }
})
</script>
