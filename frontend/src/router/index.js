import { createRouter, createWebHistory } from 'vue-router'
import SummaryPage from '../views/SummaryPage.vue'
import GuidePage from '../views/GuidePage.vue'

const routes = [
  {
    path: '/',
    name: 'Summary',
    component: SummaryPage
  },
  {
    path: '/guide',
    name: 'Guide',
    component: GuidePage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 