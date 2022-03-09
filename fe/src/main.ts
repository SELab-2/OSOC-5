import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { Quasar, Notify } from 'quasar'
import '@quasar/extras/roboto-font-latin-ext/roboto-font-latin-ext.css'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-icons-outlined/material-icons-outlined.css'
import '@quasar/extras/material-icons-round/material-icons-round.css'
import '@quasar/extras/material-icons-sharp/material-icons-sharp.css'
import '@quasar/extras/fontawesome-v5/fontawesome-v5.css'
import '@quasar/extras/mdi-v6/mdi-v6.css'
import 'quasar/src/css/index.sass'

createApp(App).use(createPinia()).use(Quasar, { plugins: { Notify }, config: { notify: {} } }).mount('#app')
