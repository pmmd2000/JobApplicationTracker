import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'

import App from './App.vue'

// PrimeVue CSS
import 'primeicons/primeicons.css'

const app = createApp(App)

// Configure PrimeVue with Aura theme
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
})

app.use(ToastService)
app.use(ConfirmationService)

app.mount('#app')
