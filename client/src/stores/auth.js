import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/axios'
import router from '@/router'

export const useAuthStore = defineStore(
  'auth',
  () => {
    let isAuthenticated = ref(false)
    let userInitials = ref('')

    async function initAuth() {
      try {
        // backend validates token stored in HTTP-only cookie (sent automatically by the browser)
        const res = await api.get('/auth/check-auth')
        
        if (res.status === 200) {
          isAuthenticated.value = true
          userInitials.value = res.data.initials
        }
      } catch (err) {
        if (isAuthenticated.value) {
          isAuthenticated.value = false
        }
      }
    }

    async function logOut() {
      try {
        const res = await api.post('auth/logout') // there is no body but we changed the state

        if (res.status === 200) {
          isAuthenticated.value = false
          router.push('/')
        }
      } catch (err) {
        console.error("Logout failed:", err)
      }
    }

    return { isAuthenticated, userInitials, initAuth, logOut }
  },
  {
    persist: true,
  },
)
