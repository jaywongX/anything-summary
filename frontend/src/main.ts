import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import { config } from './config'

const app = createApp(App)
app.use(router)
app.use(i18n)
app.config.globalProperties.$config = config
app.mount('#app') 