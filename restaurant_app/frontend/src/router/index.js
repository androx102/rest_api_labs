import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useStore } from 'vuex'


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
    component: () => import('../views/OrderDetailsView.vue')
  },
    {
    path: '/cart',
    name: 'cart',
    component: () => import('../views/CartView.vue')
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: () => import('../views/CheckoutView.vue')
  },

/*
  {
  path: '/order',
  name: 'order',
  component: () => import('../views/OrderDetailsView.vue')
},*/
{
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
  path: '/register',
  name: 'register',
  component: () => import('../views/RegisterView.vue')
},
{
  path: '/my-account',
  name: 'my-account',
  component: () => import('../views/MyAccountView.vue'),
  meta: { requiresAuth: true }
},
{
    path: '/track-order',
    name: 'track-order',
    component: () => import('../views/TrackOrderView.vue')
  },
  {
    path: '/my-orders',
    name: 'my-orders',
    component: () => import('../views/MyOrdersView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/order/:id',
    name: 'order-details',
    component: () => import('../views/OrderDetailsView.vue'),
    props: true
  },
  {
    path: '/payment-redirect/:id',
    name: 'payment-redirect',
    component: () => import('../views/PaymentRedirectView.vue'),
    props: (route) => ({
      id: route.params.id,
      email: route.query.email
    })
  }
]

const router = createRouter({
  //history: createWebHistory(process.env.BASE_URL),
  history: createWebHistory('/'),
  routes
})

router.beforeEach((to, from, next) => {
  const store = useStore()
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
