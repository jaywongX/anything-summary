import { createRouter, createWebHistory } from 'vue-router'
import SummaryPage from '../views/SummaryPage.vue'

const routes = [
  {
    path: '/',
    name: 'Summary',
    component: SummaryPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 