<template>
	<q-splitter
		v-model="splitterModel"
		:limits="[40,80]"
		style="height: 100%;"
		emit-immediately
	>
	<template #before>
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
	</q-stepper>
	<btn
		v-if="step > 0"
		style="position: absolute; left: 0; bottom:0"
		class="q-ma-md"
		@click="step -= 1"
		padding="10px"
		icon="arrow_back"
		label="Previous"
		color="yellow"
		shadow-color="orange"
	/>
	<btn
		style="position: absolute; right: 0; bottom:0"
		@click="next"
		v-if="step < 2"
		padding="10px"
		class="q-ma-md"
		icon-right="arrow_forward"
		label="Next"
		color="yellow"
		shadow-color="orange"
	>
	<q-tooltip v-if="step === 2 && !allDone" style="width: 300px">
		<span class="text-body2">
		Some data is missing.<br/>Please check if you filled in a name and partner name.
		</span>
	</q-tooltip>
	</btn>
	</template>
	<template #after>
		<div v-if="project" class="column fit justify-center items-center content-center">
			<div class="text-h6 text-bold">Preview</div>
			<project-card style="width: 90%; max-width: 400px" :project="project"/>
		</div>
	</template>
	</q-splitter>
		<btn
			style="position: absolute; right: 0; bottom:0"
			class="q-ma-md"
			v-if="basicInfoDone"
			@click="submit"
			padding="10px"
			icon-right="check"
			:label="id ? 'Update' : 'Publish'"
			color="yellow"
			shadow-color="orange"
		>
		<q-tooltip v-if="step === 2 && !allDone" style="width: 300px">
			<span class="text-body2">
			Some data is missing.<br/>Please check if you filled in a name and partner name.
			</span>
		</q-tooltip>
		</btn>
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
import ProjectCard from "./components/ProjectCard.vue"

export default defineComponent({
	name: 'CreateProject',
	components: { BasicInfo, ProjectCoaches, ProjectSkills, Overview, ProjectCard },
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
			project,
			splitterModel: ref(70)
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
			if (this.id) {
				await this.projectStore.updateProject(this.project, this.project.id)
			} else {
				await this.projectStore.addProject(this.project)
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
			return this.project?.name.length > 0 && this.project?.partnerName.length > 0 && this.project?.extraInfo.length > 0
		},
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
