<template>
	<div>
		<markdown :source="this.text" :tasklists="{enabled: true}" ref="md" breaks v-bind="$attrs"/>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Markdown from 'vue3-markdown-it'

let checkboxes = [];

export default defineComponent({
	props: {
		text: {
			type: String,
			required: true
		}
	},
	components: { Markdown },
	destroyed() {
		checkboxes.forEach(c => c.removeEventListener('click', this.onClick))
	},
	methods: {
		onClick(i: number) {
			var nth = 0;
			const newText = this.text.replace(/[-][ ]+[\[][ x][\]]/g, (match, _, original) => {
						nth++;
						if (nth === i+1) {
							return match.slice(-2) === 'x]' ? '- [ ]' : '- [x]'
						}
						return match
				})
			this.$emit('update:text', newText)
		},
	},
	watch: {
		text: {
			handler() {
				this.$nextTick(() => {
					checkboxes.forEach(c => c.removeEventListener('click', this.onClick))
					checkboxes = this.$refs.md.$el.querySelectorAll(".task-list-item-checkbox")
					checkboxes.forEach((c, i) => {
						c.addEventListener('click', () => this.onClick(i))
				})
			})
		},
		immediate: true
	}
}
})
</script>

<style scoped>

:deep(h1) {
	font-size: 1.5rem !important;
	font-weight: 600 !important;
	line-height: 100% !important;
}

:deep(h2) {
	font-size: 1.2rem !important;
	font-weight: 600 !important;
	line-height: 100% !important;
}

:deep(h3) {
	font-size: 1rem !important;
	font-weight: 600 !important;
	line-height: 100% !important;
}

:deep(h4) {
	font-size: 0.8rem !important;
	font-weight: 600 !important;
	line-height: 100% !important;
}

:deep(h5) {
	font-size: 0.7rem !important;
	font-weight: 600 !important;
	line-height: 10% !important;
}

:deep(h6) {
	font-size: 0.6rem !important;
	font-weight: 600 !important;
	line-height: 10% !important;
}

</style>