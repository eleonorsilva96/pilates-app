<script setup>
import { ref } from 'vue'
import axios from 'axios';
import { useAlertsStore } from '@/stores/alerts';
import { storeToRefs } from 'pinia';
import { showSuccessAlert, showErrorAlert } from '@/helpers/generalHelpers';
import router from '@/router';
import { useAuthStore } from '@/stores/auth';

const storeAlerts = useAlertsStore()
const storeAuth = useAuthStore()

const { isVisible, type, message } = storeToRefs(storeAlerts)
const { token } = storeToRefs(storeAuth)

const email = ref('')
const password = ref('')

// The API post request happens when the form is submitted
async function submitForm() {
  // reset alerts store array to remove old values
  type.value = []
  message.value = []

  try {
    const payload = {
      email: email.value,
      password: password.value
    }
  
    const res = await axios.post('http://localhost:8888/api/login', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (res.status === 200) {
      showSuccessAlert(res.data.message, isVisible, type, message)
      // save token in a store variable
      if (res.data.access_token) {
        token.value = res.data.access_token
        // push to index / dashboard
        router.push('/dashboard')
      } else {
        router.push('/login')
      }
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
