<template>
	<!-- v-model:selected is not used here since this displays an icon, which we don't want. As an alternative, @click is used. -->
	<!-- A Custom implementation of the icon is used, since a chip always reserves place for an icon, even when we don't want it. -->
	<q-chip
		clickable
		outline
		:color="`${skill.skill.color}-4`"
		:class="`bg-${skill.skill.color}-1`"
		:style="`border-width: 1.5px; padding-right: 8px; padding-left: ${skill.comment ? 2 : 8}px`"
		style="height: fit-content"
		@click="enabled = !enabled"
	>
		<template #default>
			<div class="column">
			<div
				class="row"
				style="display: flex; align-items: center"
			>
				<q-icon
					v-if="skill.comment"
					name="info"
					size="sm"
					:color="`${skill.skill.color}-2`"
				/>
				<div
					class="text-weight-medium"
					style="color: black;"
				>
					{{ skill.skill.name }}
				</div>
				<div
					class="text-bold"
					style="padding-left: 3px"
					:class="`text-${enabled ? 'white' : `${skill.skill.color}-8`}`"
				>
					{{ _skill.amount }}
				</div>
			</div>
			<div> 
				<q-input
					auto-grow
					outlined
				/>
			</div>
			</div>
		</template>
	</q-chip>
</template>


<script>
import {defineComponent, ref} from "vue";
import { Skill, ProjectSkill } from "../../../models/Skill"
import ProjectRoleChip from './ProjectRoleChip.vue'
export default defineComponent({
	props: {
		skill: {
			type: ProjectSkill,
			required: true
		}
	},
	components: { ProjectRoleChip },
	data() {
		console.log("created")
		return {
			open: ref(false)
		}
	},
	computed: {
		_skill: {
			get() {
				return this.skill
			},
			set(n) {
				this.$emit('update:skill', n)
			}
		}
	}
})
</script>