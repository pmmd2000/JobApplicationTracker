import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'

import App from './App.vue'

// PrimeVue CSS
import 'primeicons/primeicons.css'

// Define custom blue theme preset
const BlueTheme = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{blue.50}',
            100: '{blue.100}',
            200: '{blue.200}',
            300: '{blue.300}',
            400: '{blue.400}',
            500: '{blue.500}',
            600: '{blue.600}',
            700: '{blue.700}',
            800: '{blue.800}',
            900: '{blue.900}',
            950: '{blue.950}'
        }
    }
})

const app = createApp(App)

// Configure PrimeVue with Blue Aura theme
app.use(PrimeVue, {
    theme: {
        preset: BlueTheme,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
})

app.use(ToastService)
app.use(ConfirmationService)
import router from './router'
app.use(router)

app.mount('#app')
