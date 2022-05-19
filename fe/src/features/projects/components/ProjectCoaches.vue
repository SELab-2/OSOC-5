<template>
  <div style="overflow: hidden" class="fit column">
    <div class="row">
      <div class="text-h4">Project Coaches</div>
      <q-space />
      <q-input
        v-model="search"
        class="inputfield q-mb-sm"
        outlined
        dense
        color="teal"
        debounce="300"
        placeholder="Search"
      >
        <template #append>
          <q-icon
            v-if="search !== ''"
            name="close"
            class="cursor-pointer"
            @click="search = ''"
          />
          <q-icon v-else name="search" />
        </template>
      </q-input>
    </div>
    <div class="text-h6 row">
      <div>Selected Coaches</div>
      <q-space />
      <div>
        <btn flat round size="sm" @click="ascending = !ascending">
          <q-icon
            size="2em"
            name="arrow_downward"
            :class="ascending ? 'rotate180' : ''"
            style="
              transition: transform ease 300ms !important;
              align-self: center;
              justify-self: center;
            "
          />
        </btn>
        Available Coaches
      </div>
    </div>
    <q-splitter
      v-model="splitterModel"
      style="flex: 1; overflow: auto"
      :limits="[20, 80]"
    >
      <template #before>
        <div v-if="coaches.length === 0" class="placeholder">
          <div class="q-mb-xl">
            <lottie-animation
              animationLink="https://assets8.lottiefiles.com/packages/lf20_av8ts5jt.json"
              :height="200"
              :width="200"
              style="transform: rotate(180deg)"
            />
            <h6 class="text-bold q-mt-none q-mb-xl">
              Select a coach to add them to the project.
            </h6>
          </div>
        </div>
        <div v-else>
          <q-chip
            v-for="coach in coaches"
            :key="coach.id"
            outline
            :color="getColorFromCoach(coach)"
            class="q-pr-none q-pl-sm"
            :class="`bg-${getColorFromCoach(coach)}-1`"
            style="border-width: 1.5px; width: fit-content"
            @click="addCoachToProject(coach)"
          >
            <div class="row items-center">
              <q-icon
                style="margin-left: -6px"
                v-if="coach.projects.length > 0"
                name="info"
                size="sm"
              >
                <q-tooltip
                  v-if="coach.projects.length > 0"
                  class="text-subtitle2 text-black bg-grey-1 shadow-5 cornered"
                >
                  <span>Already assigned to the projects:</span>
                  <span v-for="project in coach.projects"
                    ><br />{{ project.name }}</span
                  >
                </q-tooltip>
              </q-icon>
              <span class="text-subtitle1 text-black">{{
                coach.fullName
              }}</span>
              <btn
                class="q-px-xs"
                size="sm"
                icon="o_delete"
                @click="removeCoachFromProject(coach)"
              />
            </div>
          </q-chip>
        </div>
      </template>
      <template #after>
        <div
          id="scroll-target-id"
          style="
            float: right;
            text-align: right;
            width: 100%;
            height: 100%;
            overflow: auto;
          "
        >
          <q-infinite-scroll
            ref="scroll"
            @load="loadNext"
            scroll-target="#scroll-target-id"
            :offset="250"
          >
            <q-chip
              v-for="(coach, i) in allCoaches"
              :key="coach.id"
              v-show="!coaches.some((c) => c.id === coach.id)"
              outline
              clickable
              :color="getColor(i)"
              :class="`bg-${getColor(i)}-1`"
              style="border-width: 1.5px"
              @click="addCoachToProject(coach)"
            >
              <div class="row" style="display: flex; align-items: center">
                <q-icon
                  style="margin-left: -11px"
                  v-if="coach.projects.length > 0"
                  name="info"
                  size="sm"
                  :color="`${getColor(i)}-6`"
                >
                  <q-tooltip
                    v-if="coach.projects.length > 0"
                    class="text-subtitle2 text-black bg-grey-1 shadow-5 cornered"
                  >
                    <span>Already assigned to the projects:</span>
                    <span v-for="project in coach.projects"
                      ><br />{{ project.name }}</span
                    >
                  </q-tooltip>
                </q-icon>
                <span class="text-subtitle1 text-black">{{
                  coach.fullName
                }}</span>
              </div>
            </q-chip>
          </q-infinite-scroll>
        </div>
      </template>
    </q-splitter>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, Ref, PropType } from 'vue'
import { useProjectStore } from '../../../stores/useProjectStore'
import { useCoachStore } from '../../../stores/useCoachStore'
import { User } from '../../../models/User'
import CreateProjectChip from './createprojectchip.vue'
import quasarColors from '../../../models/QuasarColors'
import LottieAnimation from '../../../components/LottieAnimation.vue'
export default defineComponent({
  components: { CreateProjectChip, LottieAnimation },
  props: {
    coaches: {
      type: [Object] as PropType<User[]>,
      required: true,
    },
  },
  setup() {
    const projectStore = useProjectStore()

    return {
      projectStore,
      quasarColors,
    }
  },
  data() {
    const allCoaches: Ref<User[]> = ref([])
    return {
      coachStore: useCoachStore(),
      splitterModel: ref(50),
      ascending: ref(true),
      search: ref(''),
      allCoaches,
    }
  },
  methods: {
    addCoachToProject(coach: User) {
      this.coaches.push(coach)
    },
    removeCoachFromProject(coach: User) {
      const i = this.coaches.findIndex((s) => s.id === coach.id)
      this.coaches.splice(i, 1)
    },
    getColor(i: number) {
      return this.quasarColors[i % this.quasarColors.length]
    },
    getColorFromCoach(coach: User) {
      const i = this.allCoaches.findIndex((c) => c.id === coach.id)
      return this.getColor(i)
    },
    async loadNext(i: number, done: Function) {
      let newUsers = await this.coachStore.loadNext(i, done, this.filters)
      if (i === 1) {
        this.allCoaches = []
      }
      this.allCoaches.push(...newUsers)
    },
  },
  computed: {
    filters() {
      return {
        search: this.search,
        ordering: `${this.ascending ? '' : '-'}first_name`,
      }
    },
  },
  watch: {
    filters() {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const scroll = this.$refs.scroll as any
      scroll.reset()
      scroll.resume()
      scroll.trigger()
    },
  },
})
</script>

<style scoped>
@media only screen and (min-width: 1000px) {
  .variable {
    margin: auto;
    width: 70%;
  }
}
</style>
