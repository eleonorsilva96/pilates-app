import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/axios'

export const useAuthStore = defineStore(
  'auth',
  () => {
    let isAuthenticated = ref(false)

    async function initAuth() {
      try {
        // backend validates token stored in HTTP-only cookie (sent automatically by the browser)
        const res = await api.get('/auth/check-auth')
        isAuthenticated.value = true
        console.log(res.data.message)
      } catch (err) {
        if (isAuthenticated.value) {
          isAuthenticated.value = false
        }
      }
    }

    return { isAuthenticated, initAuth }
  },
  {
    persist: true,
  },
)
