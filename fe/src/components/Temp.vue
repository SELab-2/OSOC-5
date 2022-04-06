<template>
  <div>
    <q-input
      v-model="message"
    />
    <q-btn @click="sendValue">
      Send
    </q-btn>
    {{ returnedMessage }}
  </div>
</template>
<script lang="ts">
import { defineComponent } from "@vue/runtime-core"
import { ref } from "vue"

export default defineComponent({
    setup() {
        const message = ref("")
        const returnedMessage = ref("")
        const socket = new WebSocket('ws://localhost:8000/ws/socket_server/')

        return { message, returnedMessage, socket }
    },
    mounted() {
        this.socket.onmessage = (event: { data: string }) => {
            const data = JSON.parse(event.data)
            this.returnedMessage = data.message
        }
   },   
   methods: {
       sendValue() {
        this.socket.send( JSON.stringify({
            message: this.message
        }))

        this.message = ""
       }
//        updateValue(value: string) {
           
//        }
   }
})
</script>