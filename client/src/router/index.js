import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AuthView from '../views/AuthView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import ClassesView from '../views/ClassesView.vue'
import axios from 'axios'

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

  if (!to.meta.requiresAuth) return next()

  const validateToken = async () => {
    return axios.get('http://localhost:8888/api/auth/check-auth', { withCredentials: true }) // send cookies along with cross-origin requests
  }

  try {
    // backend validates token stored in HTTP-only cookie (sent automatically by the browser)
    const res = await validateToken()
    console.log(res.data.message)
    next()
  } catch (err) {
    // if access token expires read refresh token to create another one in route /refresh
    if (err.response?.status === 401) {
        try {
          const res = await axios.get('http://localhost:8888/api/auth/refresh', { withCredentials: true })
          console.log(res.data.message)
          next()
        } catch (err) {
          // if refresh token is expired send user to the login page
          next('/auth/login')
        }
    } else {
      next('/auth/login')
    }
    
  }
})

export default router
