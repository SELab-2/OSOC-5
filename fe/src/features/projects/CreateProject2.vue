<template>
	<!-- <div> -->
	<q-stepper
		v-model="step"
		color="primary"
		class="column"
		style="height: 100%"
		animated
		keep-alive
		header-nav
		flat
	>
		<q-step
			:name="1"
			title="Project Info"
			icon="settings"
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
			icon="create_new_folder"
			:done="coachesDone"
		>
			<ProjectCoaches :coaches="project.coaches"/>
		</q-step>

		<q-step
			:name="3"
			title="Skills"
			icon="assignment"
			:done="skillsDone"
		>
			<ProjectSkills :skills="project.requiredSkills"/>
		</q-step>

		<q-step
			:name="4"
			title="Overview"
			icon="add_comment"
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
			:label="step < 4 ? 'Next' : 'Submit'"
			:disable="step === 3 && !allDone"
			color="yellow"
			shadow-color="orange"
		/>
	</q-page-sticky>
	<!-- </div> -->
</template>

<script>
import { ref } from 'vue'
import BasicInfo from "./components/BasicInfo.vue";
import ProjectCoaches from "./components/ProjectCoaches.vue";
import ProjectSkills from "./components/ProjectSkills.vue";
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'
import { useProjectStore } from '../../stores/useProjectStore'

import { Project } from '../../models/Project'
import Overview from "./components/CreateOverview.vue"
export default {
	name: 'CreateProject',
	components: { BasicInfo, ProjectCoaches, ProjectSkills, Overview },
	props: {
		id: {
			type: String,
			required: false
		}
	},
	data() {
		const project = useProjectStore().projects.find(p => p.id === parseInt(this.id)) ?? new Project('','','',0,[],[],[])
		console.log(project)
		console.log(useProjectStore().projects.find(p => p.id === parseInt(this.id)))
		return {
			step: ref(1),
			skillStore: useSkillStore(),
			coachStore: useCoachStore(),
			projectStore: useProjectStore(),
			project: ref(project)
		}
	},
	mounted(){
		this.skillStore.loadSkills()
		this.coachStore.loadUsers()
	},
	methods: {
		next() {
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
				this.projectStore.addProject(mappedProject)
			}
		}
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
}
</script>

<style scoped>

:deep(.q-stepper__content) {
	flex: 1
}

:deep(.q-stepper__step-content), :deep(.q-stepper__step-inner) {
	height: 100%
}


</style>
