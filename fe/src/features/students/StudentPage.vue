<template>
  <SideBar
    :key="sideBarKey"
    color="bg-grey-3"
    :select-student="selectStudent"
    :draggable="false"
  />

  <div
    :key="studentKey"
    class="justify-between row q-px-lg q-pt-lg studentcol"
  >
    <div class="row q-pa-sm q-gutter-sm items-center">
      <h class="text-bold text-h4">
        {{ name }}
      </h>
      <q-btn
        :href="student ? student.cv.toString() : ''"
        target="_blank"
        size="12px"
        rounded
        outline
        color="black"
        label="CV"
      />
      <q-btn
        :href="student ? student.portfolio.toString() : ''"
        target="_blank"
        size="12px"
        rounded
        outline
        color="black"
        label="Portfolio"
      />
    </div>
    <div
      v-if="authenticationStore.loggedInUser?.isAdmin ?? false"
      class="row q-gutter-sm items-center"
    >
      <q-select
        v-model="possibleFinalDecision"
        emit-value
        map-options
        rounded
        outlined
        dense
        style="width: 200px"
        :options="[
          { value: '0', label: 'Yes' },
          { value: '2', label: 'Maybe' },
          { value: '1', label: 'No' },
          { value: '-1', label: 'Not decided' },
        ]"
        label="Final decision"
      />
      <q-btn
        icon-right="mail"
        class="cornered"
        label="Confirm"
        outline
        color="black"
        @click="finalDecision"
      />
    </div>
  </div>

  <div class="row q-px-lg q-ml-sm q-mt-sm items-center">
    <label>Suggest:</label>
  </div>
  <div class="row q-px-lg q-ml-sm items-center">
    <SegmentedControl
      v-model="mySuggestion"
      :color="mySuggestionColor"
      :options="[
        { name: '0', label: 'Yes' },
        { name: '2', label: 'Maybe' },
        { name: '1', label: 'No' },
        { name: '-1', label: 'Not decided' },
      ]"
      @update:modelValue="showDialog"
    />

    <<<<<<< HEAD
    <q-dialog v-model="suggestionDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">
            Suggest
            <btn
              dense
              rounded
              class="text-h6"
              :class="suggestionColor"
            >
              {{ suggestionName }}
            </btn>
            =======
            <q-dialog v-model="suggestionDialog">
              <q-card>
                <q-card-section>
                  {{ suggestionName }}
                  {{ suggestionColor }}
                  <div class="text-h6">
                    Suggest
                    <btn
                      :label="suggestionName"
                      dense
                      rounded
                      class="text-h6"
                      :class="suggestionColor"
                    />
                    >>>>>>> main
                    for {{ name }}
                  </div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                  Why are you making this decision? (optional)
                  <q-input
                    v-model="reason"
                    filled
                    type="textarea"
                  />
                </q-card-section>

                <q-card-actions
                  align="right"
                  class="text-primary"
                >
                  <btn
                    v-close-popup
                    flat
                    color="grey"
                    label="Cancel"
                    glow-color="grey-4"
                  />
                  <btn
                    v-close-popup
                    flat
                    label="Suggest"
                    glow-color="teal-1"
                    @click="makeSuggestion"
                  />
                </q-card-actions>
              </q-card>
            </q-dialog>
          </div>

          <div class="q-gutter-sm q-pa-lg">
            <div class="row">
              <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
                <SuggestionsCard
                  :index="studentKey"
                  title="Suggestions"
                />
              </div>
              <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
                <AcademiaCard
                  :index="studentKey"
                  title="Academia"
                />
              </div>
              <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">
                <SkillsCard
                  :index="studentKey"
                  title="Skills"
                />
              </div>
            </div>
            <div class="row">
              <div class="studentcol col-12">
                <ExtraInfoCard
                  :index="studentKey"
                  title="Extra Info"
                />
              </div>
            </div>
            <!--    <div class="row">-->
            <!--      <div class="studentcol col-12">-->
            <!--        <TitleTextCard title="Project you're most proud of" content="-->
            <!--            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."-->
            <!--        />-->
            <!--      </div>-->
            <!--    </div>-->
            <!--    <div class="row">-->
            <!--      <div class="studentcol col-xs-12 col-sm-12 col-md-8 col-lg-8">-->
            <!--        <PracticalCard title="Practical"/>-->
            <!--      </div>-->
            <!--      <div class="studentcol col-xs-12 col-sm-12 col-md-4 col-lg-4">-->
            <!--        <DetailsCard title="Details" :content="[-->
            <!--            { description: 'First language', value: 'English'},-->
            <!--            { description: 'Level of English', value: '1/5'}-->
            <!--          ]"/>-->
            <!--      </div>-->
            <!--    </div>-->
            <!--    <div class="row">-->
            <!--      <div class="studentcol col-xs-12 col-sm-12 col-md-6 col-lg-6">-->
            <!--        <TitleTextCard title="Why do you want to participate in osoc?" content="-->
            <!--            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."-->
            <!--        />-->
            <!--      </div>-->
            <!--      <div class="studentcol col-xs-12 col-sm-12 col-md-6 col-lg-6">-->
            <!--        <TitleTextCard title="Why do you think you're a good fit?" content="-->
            <!--            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."-->
            <!--        />-->
            <!--      </div>-->
            <!--    </div>-->
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import {useAuthenticationStore} from "../../stores/useAuthenticationStore";
import {useStudentStore} from "../../stores/useStudentStore";
import {ref} from "vue";
import SideBar from "../../components/SideBar.vue"
import AcademiaCard from "./components/AcademiaCard.vue";
import SkillsCard from "./components/SkillsCard.vue";
import SuggestionsCard from "./components/SuggestionsCard.vue";
import SegmentedControl from "../../components/SegmentedControl.vue"
import { Student } from "../../models/Student";
import {defineComponent} from "@vue/runtime-core";
import ExtraInfoCard from "./components/ExtraInfoCard.vue";

export default defineComponent ({
  components: {
    ExtraInfoCard,
    AcademiaCard,
    SuggestionsCard,
    SkillsCard,
    SegmentedControl,
    SideBar,
  },
  props: {
    id: {
      type: String,
      required: true
    },
  },
  setup() {
    const authenticationStore = useAuthenticationStore()
    const studentStore = useStudentStore()

    return {
      authenticationStore,
      studentStore,
      possibleFinalDecision: ref("-1"),
    }
  },
  data() {
    const suggestionDialog = ref(false)
    const reason = ref("")

    return {
      sideBarKey: 0,
      studentKey: 0,
      suggestionDialog,
      reason
    }
  },
  computed: {
    student(): Student | null {
      return this.studentStore.currentStudent
    },
    possibleSuggestion(): string {
      return this.studentStore.possibleSuggestion.toString()
    },
    name(): string {
      return this.student ? this.student.firstName + ' ' + this.student.lastName : ""
    },
    mySuggestion(): string {
      if (! this.studentStore.isLoading && this.student) {
        const mySuggestions = this.student.suggestions.filter(suggestion => suggestion.coachId === this.authenticationStore.loggedInUser?.id)

        return mySuggestions.length > 0 ? mySuggestions[0].suggestion.toString() : (-1).toString()
      } else {
        return this.possibleSuggestion.toString()
      }

    },
    mySuggestionColor(): string {
      let mySuggestion = this.mySuggestion
      switch (mySuggestion) {
        case "0":
          return "green"
        case "1":
          return "red"
        case "2":
          return "yellow"
        default:
          return "grey"
      }
    },
    suggestionName(): string {
      switch (this.possibleSuggestion) {
        case "0":
          return "yes"
        case "1":
          return "no"
        case "2":
          return "maybe"
        default:
          return "not decided"
      }
    },
    suggestionColor(): string {
      switch (this.possibleSuggestion) {
        case "0":
          return "bg-green"
        case "1":
          return "bg-red"
        case "2":
          return "bg-yellow"
        default:
          return "bg-grey"
      }
    }
  },
  mounted() {
    // Reload when new student is selected
    this.$watch('id', async (id: number) => {
      await this.studentStore.loadStudent(id)

      if (this.student?.finalDecision) {
        this.possibleFinalDecision = this.student.finalDecision.suggestion.toString()
      } else {
        this.possibleFinalDecision = (-1).toString()
      }
    }, {immediate: true})
  },
  methods: {
    makeSuggestion: async function () {
      if (this.student) {
        await this.studentStore.updateSuggestion(this.student.id, (this.authenticationStore?.loggedInUser?.id) || -1, this.possibleSuggestion, this.reason)
        this.reason = ""
      }

      // Make components update
      this.sideBarKey += 1
      this.studentKey += 1
    },
    selectStudent: function (selected_student: Student) {
      this.$router.push(`/students/${selected_student.id}`)
    },
    showDialog: function (value: number) {
      this.studentStore.possibleSuggestion = value
      this.suggestionDialog = true
    },
    finalDecision: async function () {
      if (this.student) {
        await this.studentStore.updateFinalDecision(this.student.id, this.possibleFinalDecision)
      }

      // Make components update
      this.sideBarKey += 1
      this.studentKey += 1
    }
  },
})
</script>
