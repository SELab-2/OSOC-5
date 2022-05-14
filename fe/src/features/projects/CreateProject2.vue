<template>
	<div class="q-pa-md">
		<q-stepper
			v-model="step"
			color="primary"
			animated
			keep-alive
			header-nav
			flat
		>
			<q-step
				:name="1"
				title="Project Info"
				icon="settings"
				:done="step > 1"
			>
				<div class="column">
					First, some basic info!
					<BasicInfo
						v-model:name="name"
						v-model:partnerName="partnerName"
						v-model:info="info"
					/>
				</div>

				<q-stepper-navigation>
					<q-btn @click="step = 2" color="primary" label="Continue" />
				</q-stepper-navigation>
			</q-step>

			<q-step
				:name="2"
				title="Coaches"
				caption="Optional"
				icon="create_new_folder"
				:done="step > 2"
			>
				<ProjectCoaches />

				<q-stepper-navigation>
					<q-btn @click="step = 3" color="primary" label="Continue" />
					<q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm" />
				</q-stepper-navigation>
			</q-step>

			<q-step
				:name="3"
				title="Skills"
				icon="assignment"
			>
				<ProjectSkills/>
			</q-step>

			<q-step
				:name="4"
				title="Overview"
				icon="add_comment"
				disable
			>
				Try out different ad text to see what brings in the most customers, and learn how to
				enhance your ads using features like ad extensions. If you run into any problems with
				your ads, find out how to tell if they're running and how to resolve approval issues.

				<q-stepper-navigation>
					<q-btn color="primary" label="Finish" />
					<q-btn flat @click="step = 2" color="primary" label="Back" class="q-ml-sm" />
				</q-stepper-navigation>
			</q-step>
		</q-stepper>
	</div>
</template>

<script>
import { ref } from 'vue'
import BasicInfo from "./components/BasicInfo.vue";
import ProjectCoaches from "./components/ProjectCoaches.vue";
import ProjectSkills from "./components/ProjectSkills.vue";
import { useSkillStore } from '../../stores/useSkillStore'
import { useCoachStore } from '../../stores/useCoachStore'
export default {
	setup () {
		return {
			step: ref(1),
			skillStore: useSkillStore(),
			coachStore: useCoachStore()
		}
	},
	components: { BasicInfo, ProjectCoaches, ProjectSkills },
	data() {
		return {
			name: ref(''),
			partnerName: ref(''),
			info: ref('')
		}
	},
	mounted(){
		this.skillStore.loadSkills()
		this.coachStore.loadUsers()
	}
}
</script>
