<template>
	<!-- <div> -->
	<q-stepper
		v-if="project"
		v-model="step"
		class="column"
		style="height: 100%"
		active-icon="none"
		done-color="teal"
		active-color="teal"
		animated
		keep-alive
		header-nav
		flat
	>
		<q-step
			:name="1"
			title="Project Info"
			icon="r_info"
			:done="basicInfoDone"
		>
			<BasicInfo
				v-model:name="project.name"
				v-model:partnerName="project.partnerName"
				v-model:info="project.extraInfo"
			/>
		</q-step>

		<q-step
			:name="2"
			title="Coaches"
			caption="Optional"
			icon="r_group"
			:done="coachesDone"
		>
			<ProjectCoaches :coaches="project.coaches"/>
		</q-step>

		<q-step
			:name="3"
			title="Skills"
			icon="r_build"
			:done="skillsDone"
		>
			<ProjectSkills :skills="project.requiredSkills"/>
		</q-step>

		<q-step
			:name="4"
			title="Overview"
			icon="r_receipt_long"
			:disable="!allDone"
		>
			<overview :project="project"/>
		</q-step>
	</q-stepper>
	<q-page-sticky position="bottom-right" :offset="[18, 18]">
		<btn
			fab
			@click="next()"
			padding="10px"
			:icon-right="step < 4 ? 'arrow_forward' : 'check'"
			:label="step < 4 ? 'Next' : (id ? 'Update' : 'Submit')"
			:disable="step === 3 && !allDone"
			color="yellow"
			shadow-color="orange"
		>
		<q-tooltip v-if="step === 3 && !allDone" style="width: 300px">
			<span class="text-body2">
			Some data is missing.<br/>Please check if you filled in a name, partner name, info, and have selected at least one skill and coach.
			</span>
		</q-tooltip>
		</btn>
	</q-page-sticky>
	<q-page-sticky position="bottom-left" :offset="[18, 18]">
		<btn
			v-if="step > 1"
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
			step: ref(1),
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
		async next() {
			if (this.step < 4) {
				this.step += 1
			} else {
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
	},
	computed: {
		basicInfoDone() {
			return this.project.name.length > 0 && this.project.partnerName.length > 0
		},
		coachesDone() {
			return this.project.coaches.length > 0
		},
		skillsDone() {
			return this.project.requiredSkills.length > 0
		},
		allDone() {
			return this.basicInfoDone && this.coachesDone && this.skillsDone
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
