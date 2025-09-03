import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import ClassesView from '../views/ClassesView.vue'
import { useAuthStore } from '../stores/auth'
import { storeToRefs } from 'pinia'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/auth',
      component: AuthView,
      children: [
        { path: 'login', name: 'login', component: LoginView },

        { path: 'register', name: 'register', component: RegisterView },
      ],
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }, // protected route
    },
    {
      path: '/classes',
      name: 'classes',
      component: ClassesView,
      meta: { requiresAuth: true }, // protected route
    },
  ],
})

// before the route changes to protected routes check if user is authenticated
router.beforeEach(async (to, from, next) => {
  const storeAuth = useAuthStore() // initialize auth store after pinia is created
  const { isAuthenticated } = storeToRefs(storeAuth)

  if (isAuthenticated.value && to.name === 'home')
    return next() // allow authenticated users to access home
  else if (isAuthenticated.value && !to.meta.requiresAuth)
    return next('/dashboard') // redirect authenticated users from other public pages
  else if (isAuthenticated.value)
    return next() // allow authenticated users to access protected pages
  else if (!isAuthenticated.value && to.meta.requiresAuth)
    return next('/auth/login') // redirect unauthenticated users from protected pages
  else return next() // allow unauthenticated users to access public pages
})

export default router
