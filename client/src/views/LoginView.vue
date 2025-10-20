<script setup>
import { ref } from 'vue'
import router from '@/router'
import api from '@/services/axios'
import { useAlertsStore } from '@/stores/alerts'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { showSuccessAlert, showErrorAlert } from '@/helpers/generalHelpers'

const email = ref('')
const password = ref('')

// The API post request happens when the form is submitted
async function submitForm() {
  const storeAlerts = useAlertsStore()
  const storeAuth = useAuthStore()

  const { isVisible, type, message } = storeToRefs(storeAlerts)
  const { isAuthenticated } = storeToRefs(storeAuth)

  // reset alerts store array to remove old values
  type.value = []
  message.value = []

  try {
    const payload = {
      email: email.value,
      password: password.value,
    }

    const res = await api.post('/auth/login', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // TO DO: reset submit form fields
    // TO DO: disabled submit button while awaiting for API response to prevent double submissions
    if (res.status === 200) {
      showSuccessAlert(res.data.message, isVisible, type, message)
      storeAuth.initAuth()
      isAuthenticated.value = true
      router.push('/dashboard')
    }
  } catch (err) {
    // insert errors messages to the front
    if (err.response) {
      showErrorAlert(err, isVisible, type, message)
    } else {
      console.error('Failed to fetch message:', err)
    }
  }
}
</script>

<template>
  <form action="/login" method="post" @submit.prevent="submitForm">
    <div class="flex flex-col w-full gap-4">
      <div class="flex flex-col gap-2">
        <label for="email" class="text-sm font-medium text-opacity-75">Email</label>
        <input
          autocomplete="off"
          v-model="email"
          placeholder="Enter your email"
          type="text"
          class="h-10 border rounded-md px-3 py-2 text-base focus:outline-none focus:border-2 focus:border-pink-400 focus:px-4 focus:py-3"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="password" class="text-sm font-medium text-opacity-75">Password</label>
        <input
          autocomplete="off"
          v-model="password"
          placeholder="Enter your password"
          type="password"
          class="h-10 border rounded-md px-3 py-2 text-base focus:outline-none focus:border-2 focus:border-pink-400"
        />
      </div>
      <button
        class="w-full text-white bg-pink-700 hover:bg-pink-800 focus:ring-4 focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-pink-600 dark:hover:bg-pink-700 focus:outline-none dark:focus:ring-pink-800"
      >
        Login
      </button>
    </div>
  </form>
</template>
