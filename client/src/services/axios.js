// axios instance with a interceptor attached

import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const api = axios.create({
  baseURL: 'http://localhost:8888/api',
  withCredentials: true,
})

api.interceptors.response.use(
  (response) => response,
  async (err) => {
    const authStore = useAuthStore()
    const { isAuthenticated } = storeToRefs(authStore)

    // if access token expires read refresh token to create another one in route /refresh
    // do refresh requests only if the user is authenticated
    if (err.response?.status === 401 && isAuthenticated.value) {
      try {
        const res = await axios.get('http://localhost:8888/api/auth/refresh', {
          withCredentials: true,
        })
        isAuthenticated.value = true
        console.log(res.data.message)

        return axios(err.config) // retry original request with new token backend refreshed
      } catch (err) {
        // if refresh token is expired send user to the login page
        isAuthenticated.value = false
        window.location.href = 'auth/login'
      }
    }

    return Promise.reject(err)
  },
)

export default api
