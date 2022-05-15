<template>
	<div>
		<project-card :project="project"/>
	</div>
</template>

<script>
import { defineComponent } from 'vue'
import { Project } from "../../../models/Project"
import ProjectCard from "./ProjectCard.vue"

export default defineComponent({
	props: {
		project: {
			type: Project,
			required: true
		}
	},
	components: { ProjectCard }
})

</script>