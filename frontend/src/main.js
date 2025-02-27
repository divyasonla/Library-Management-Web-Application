import './index.css'

import { createApp } from 'vue'
import router from './router'
import App from './App.vue'

import {
  Button,
  Card,
  Input,
  setConfig,
  frappeRequest,
  resourcesPlugin,
} from 'frappe-ui'

// FontAwesome Imports
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPen, faTrash, faPlus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import './registerServiceWorker'

// Icons ko library mein add karo
library.add(faPen, faTrash, faPlus)

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)

app.use(router)
app.use(resourcesPlugin)

app.component('Button', Button)
app.component('Card', Card)
app.component('Input', Input)

// Register FontAwesome Icon Component
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
