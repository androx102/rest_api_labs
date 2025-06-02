import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/menu',
    name: 'menu',
    component: () => import('../views/MenuView.vue')
  },
    {
      //this is for "my orders" page
    path: '/order',
    name: 'order',
    component: () => import('../views/OrderView.vue')
  },
    {
    path: '/cart',
    name: 'cart',
    component: () => import('../views/CartView.vue')
  }
]

const router = createRouter({
  //history: createWebHistory(process.env.BASE_URL),
  history: createWebHistory('/'),
  routes
})

export default router
