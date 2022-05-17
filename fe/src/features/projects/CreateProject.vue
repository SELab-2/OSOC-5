<template>
	<!-- <div> -->
	<q-stepper
		v-if="project"
		v-model="step"
		class="column"
		style="height: 100%"
		active-icon="none"
		error-icon="none"
		done-color="teal"
		active-color="teal"
		error-color="yellow"
		animated
		keep-alive
		header-nav
		flat
	>
		<q-step
			:name="0"
			title="Project Info"
			icon="r_info"
			:done="basicInfoDone"
			:caption="visitedSteps[0] && !basicInfoDone ? 'Empty Fields Left' : project?.name"
			
		>
			<BasicInfo
				v-model:name="project.name"
				v-model:partnerName="project.partnerName"
				v-model:info="project.extraInfo"
			/>
		</q-step>

		<q-step
			:name="1"
			title="Coaches"
			icon="r_group"
			:done="coachesDone"
			:caption="`${project?.coaches.length} Coach${project?.coaches.length !== 1 ? 'es' : ''} Selected`"
		>
			<ProjectCoaches :coaches="project.coaches"/>
		</q-step>

		<q-step
			:name="2"
			title="Skills"
			icon="r_build"
			:done="skillsDone"
			:caption="`${project?.requiredSkills.length} Skill${project?.requiredSkills.length !== 1 ? 's' : ''} Selected`"
		>
			<ProjectSkills :skills="project.requiredSkills"/>
		</q-step>

		<q-step
			:name="3"
			title="Overview"
			icon="r_receipt_long"
			:disable="!allDone"
			:caption="visitedSteps[3] && !allDone ? 'Empty Fields Left' : ''"
		>
			<overview :project="project"/>
		</q-step>
	</q-stepper>
	<q-page-sticky position="bottom-right" :offset="[18, 18]">
		<btn
			fab
			v-if="id && step < 3"
			@click="submit"
			padding="10px"
			icon-right="check"
			label="Update"
			color="yellow"
			shadow-color="orange"
			class="q-mr-sm"
		/>
		<btn
			fab
			@click="next"
			padding="10px"
			:icon-right="step < 3 ? 'arrow_forward' : 'check'"
			:label="step < 3 ? 'Next' : (id ? 'Update' : 'Submit')"
			:disable="step === 2 && !allDone"
			color="yellow"
			shadow-color="orange"
		>
		<q-tooltip v-if="step === 2 && !allDone" style="width: 300px">
			<span class="text-body2">
			Some data is missing.<br/>Please check if you filled in a name and partner name.
			</span>
		</q-tooltip>
		</btn>
	</q-page-sticky>
	<q-page-sticky position="bottom-left" :offset="[18, 18]">
		<btn
			v-if="step > 0"
			fab
			@click="step -= 1"
			padding="10px"
			icon="arrow_back"
			label="Previous"
			color="yellow"
			shadow-color="orange"
		/>
	</q-page-sticky>
	<!-- </div> -->
</template>

<script>
import { ref, defineComponent } from 'vue'
import BasicInfo from "./components/BasicInfo.vue";
import ProjectCoaches from "./components/ProjectCoaches.vue";
import ProjectSkills from "./components/ProjectSkills.vue";
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'
import { useProjectStore } from '../../stores/useProjectStore'
import { Project } from '../../models/Project'
import Overview from "./components/CreateOverview.vue"
import router from '../../router'

export default defineComponent({
	name: 'CreateProject',
	components: { BasicInfo, ProjectCoaches, ProjectSkills, Overview },
	props: {
		id: {
			type: String,
			required: false
		}
	},
	data() {
		const projectStore = useProjectStore();
		const project = ref(null);
		return {
			step: ref(0),
			visitedSteps: ref([false, false, false, false]),
			skillStore: useSkillStore(),
			coachStore: useCoachStore(),
			projectStore: useProjectStore(),
			project
		}
	},
	async created() {
		let project;
		if (this.id) {
			try {
				project = await this.projectStore.getProject(this.id)
			} catch (error) {
				router.replace('/notfound')
			}
		} else {
			project = new Project('','','',0,[],[],[])
		}
		return this.project = project
	},
	mounted(){
		this.skillStore.loadSkills()
		this.coachStore.loadUsers()
	},
	methods: {
		next() {
			if (this.step < 3) {
				this.step += 1
			} else {
				this.submit()
			}
		},
		async submit() {
			const mappedProject = {
				name: this.project.name,
				partnerName: this.project.partnerName,
				extraInfo: this.project.extraInfo,
				requiredSkills: this.project.requiredSkills.map(s => {
					return {
						amount: s.amount,
						comment: s.comment,
						skill: s.skill.url
					}
				}),
				coaches: this.project.coaches.map(c => c.url),					
			}
			if (this.id) {
				await this.projectStore.updateProject(mappedProject, this.project.id)
			} else {
				await this.projectStore.addProject(mappedProject)
			}
			this.projectStore.shouldRefresh = true
			router.replace('/projects')
		}
	},
	watch: {
		step(newValue, oldValue) {
			this.visitedSteps[oldValue] = true
		}
	},
	computed: {
		basicInfoDone() {
			return this.project.name.length > 0 && this.project.partnerName.length > 0 && this.project.extraInfo.length > 0
		},
		coachesDone() {
			return this.project.coaches.length > 0
		},
		skillsDone() {
			return this.project.requiredSkills.length > 0
		},
		allDone() {
			return this.basicInfoDone
		}
	}
})
</script>

<style scoped>

:deep(.q-stepper__content) {
	flex: 1
}

:deep(.q-stepper__step-content), :deep(.q-stepper__step-inner) {
	height: 100%
}


</style>
