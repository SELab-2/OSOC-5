<template>
	<div>
		<project-card :project="project" style="max-width: 400px; margin: auto"/>
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