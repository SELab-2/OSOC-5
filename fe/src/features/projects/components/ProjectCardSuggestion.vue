<template>
  <!-- appear only when a new entry is added. Otherwise, the suggestions may be glitchy when removing suggestions. -->
  <q-slide-transition
    :appear="(fromLocal || fromWebsocket) && !suggestion.reason"
  >
    <div v-if="show" style="margin-left: 10px">
      <div class="column full-width">
        <div
          :lines="1"
          tabindex="-1"
          class="row flex-center no-wrap"
          style="height: 30px"
        >
          <div
            class="text-weight-medium row wrap text-no-wrap"
            :class="removed ? 'text-strike' : ''"
          >
            {{ suggestion.student.firstName }}
            {{ suggestion.student.lastName }}
          </div>
          <q-badge
            v-if="fromWebsocket || fromLocal"
            rounded
            :color="suggestion.skill.color"
            :label="fromWebsocket ? 'New' : 'Draft'"
            class="q-ml-xs"
          />

          <q-space />
          <div
            v-if="!removed"
            style="flex-wrap: nowrap; display: block; min-width: 48px"
          >
            <btn
              tabindex="-1"
              class="gt-xs"
              size="sm"
              flat
              dense
              round
              icon="r_person"
              :to="`/students/${suggestion.student.id}`"
            />
            <btn
              v-if="!fromLocal"
              tabindex="-1"
              class="gt-xs"
              size="sm"
              flat
              dense
              round
              icon="r_info"
              @mouseover="
                () => {
                  if (progress === 0) progress = 3
                }
              "
              @mouseleave="
                () => {
                  if (progress === 3) progress = 0
                }
              "
              @click="disableHover = !disableHover"
            />
            <btn
              tabindex="-1"
              class="gt-xs"
              size="sm"
              flat
              dense
              round
              icon="delete"
              @click="
                () => {
                  removed = true
                  fromLocal ? remove() : prepareRemove()
                }
              "
            />
          </div>
          <btn
            v-else
            label="undo"
            dense
            style="justify-content: center; height: 30px"
            @click="stop"
          />
        </div>
        <q-slide-transition>
          <div v-if="progress === 3 || disableHover" style="margin-left: 10px">
            <div>Assigned by {{ suggestion.coach.fullName }}</div>
            <div v-if="suggestion.reason">
              <div class="text-bold">Comment</div>
              {{ suggestion.reason }}
            </div>
            <div v-else>No comment provided</div>
          </div>
        </q-slide-transition>
        <q-slide-transition v-if="progress >= 0">
          <q-input
            v-if="fromLocal || (progress !== 0 && progress !== 3)"
            v-model="localSuggestion.reason"
            autofocus
            :color="suggestion.skill.color"
            dense
            outlined
            autogrow
            label="Comment (Optional)"
          >
            <template #after>
              <btn
                :color="progress === 2 ? 'positive' : suggestion.skill.color"
                dense
                flat
                focusable
                padding="sm"
                :loading="progress === 1"
                :icon="progress === 0 ? 'r_send' : 'r_check'"
                :glow-color="
                  progress === 2 ? 'green-2' : `${suggestion.skill.color}-2`
                "
                @click="confirm"
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
            @click="
              () => {
                progress = 1
                confirm()
              }
            "
          />
        </div>
      </div>
    </div>
  </q-slide-transition>
</template>

<!-- A component which displays a student in a project. -->
<script lang="ts">
import { defineComponent, ref } from 'vue'
import {
  ProjectSuggestion,
  NewProjectSuggestion,
} from '../../../models/ProjectSuggestion'
import { useProjectStore } from '../../../stores/useProjectStore'

export default defineComponent({
  props: {
    // Function to run when a suggesiton is confirmed, and can be sent to the backend.
    confirmSuggestion: {
      type: Function,
      required: true,
    },
    // Function to run when a suggestion can be removed.
    removeSuggestion: {
      type: Function,
      required: true,
    },
    // A suggestion.
    suggestion: {
      type: ProjectSuggestion,
      required: true,
    },
  },
  data() {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let timeout: any | null = null
    return {
      projectStore: useProjectStore(),
      show: ref(true),
      progress: ref(0),
      removed: ref(false),
      disableHover: ref(false),
      timeout,
      localSuggestion: this.suggestion,
    }
  },
  computed: {
    // This returns true if the suggestion has been recently added (locally, or by another user).
    // This a the "draft" suggesiton.
    isNew() {
      return this.suggestion instanceof NewProjectSuggestion
    },
    // This returns true if the suggestion has been recently added locally (displayed as "draft") and has not yet been pushed to the server.
    fromLocal() {
      return this.isNew && (this.suggestion as NewProjectSuggestion).fromLocal
    },
    // This returns true if the suggestion has been recently added by another user (displayed as "new").
    fromWebsocket() {
      return (
        this.isNew && (this.suggestion as NewProjectSuggestion).fromWebsocket
      )
    },
  },
  // Remove any leftover planned student removals.
  beforeUnmount() {
    if (this.timeout) {
      clearTimeout(this.timeout)
      this.remove()
    }
  },
  methods: {
    // When the user clicks the undo button, this cancels the removal of a student.
    stop() {
      this.removed = false
      if (!this.timeout) return
      clearTimeout(this.timeout)
      this.timeout = null
    },

    // This shows the undo button for a short period of time, and will call the actual remove method after a short period of time.
    prepareRemove() {
      this.timeout = setTimeout(() => {
        this.remove()
        this.timeout = null
      }, 2000)
    },

    // Actually removes the suggestion from the server. If the suggestion is a draft, it only gets removed locally.
    remove() {
      this.show = false
      // A short timeout is added to play the remove animation.
      setTimeout(() => {
        this.removeSuggestion(this.suggestion)
      }, 500)
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
})
</script>
