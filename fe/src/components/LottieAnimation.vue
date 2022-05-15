<template>
	<Vue3Lottie v-bind="$attrs" :pauseAnimation="playing" />
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
	data() {
		return {
			playing: ref(false)
		}
	},
	activated() {
		console.log("starting")
		this.playing = false
	},
	deactivated() {
		console.log("stopping")

		this.playing = true
	}
})
</script>