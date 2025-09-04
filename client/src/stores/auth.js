import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/axios'

export const useAuthStore = defineStore(
  'auth',
  () => {
    let isAuthenticated = ref(false)
    let userInitials = ref([])

    async function initAuth() {
      try {
        // backend validates token stored in HTTP-only cookie (sent automatically by the browser)
        const res = await api.get('/auth/check-auth')
        isAuthenticated.value = true

        if (res.status === 200) {
          userInitials.value = res.data.initials
          console.log(userInitials)
        }
      } catch (err) {
        if (isAuthenticated.value) {
          isAuthenticated.value = false
        }
      }
    }

    return { isAuthenticated, userInitials, initAuth }
  },
  {
    persist: true,
  },
)
