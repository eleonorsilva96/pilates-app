<script setup>
import { computed, reactive, ref, watch } from 'vue'
import axios from 'axios'
import { useAlertsStore } from '@/stores/alerts'
import { storeToRefs } from 'pinia'
import { showAlert } from '@/helpers/generalHelpers'
import { isValidEmail, isValidName } from '@/helpers/textHelpers'

const storeAlerts = useAlertsStore()
const { isVisible, type, message } = storeToRefs(storeAlerts)
const fullname = ref('')
const email = ref('')
const password = ref('')
const code = ref(0)
let isDisabled = ref(true)

const styleStates = reactive({
  fullnameBorder: 'focus:border-pink-400 focus:border-2',
  emailBorder: 'focus:border-pink-400 focus:border-2',
  passwordBorder: 'focus:border-pink-400 focus:border-2',
  disabledButton: 'opacity-50'
})

// allow only letters in the name 
watch(fullname, (newVal) => {
  if (newVal !== '' && !isValidName(newVal)) {
    styleStates.fullnameBorder = 'border-red-500 border-2'
    type.value = 'error'
    message.value = 'Only letters are allowed in the name'
    showAlert(isVisible)
    } else {
      styleStates.fullnameBorder = 'focus:border-pink-400 focus:border-2'
    }
})

// check for email format
watch(email, (newVal) => {
  if (newVal !== '' && !isValidEmail(newVal)) {
    styleStates.emailBorder = 'border-red-500 border-2'
    type.value = 'error'
    message.value = 'Enter a valid email'
    showAlert(isVisible)
  } else {
    styleStates.emailBorder = 'focus:border-pink-400 focus:border-2'
  }
})

// check if password is at least 5 characters
watch(password, (newVal) => {
  if (newVal !== '' && newVal.length < 5) {
    styleStates.passwordBorder = 'border-red-500 border-2'
    type.value = 'error'
    message.value = 'Enter a password with at least 5 characters'
    showAlert(isVisible)
  } else {
    styleStates.passwordBorder = 'focus:border-pink-400 focus:border-2'
  }
})

// disable button until the input value is not empty
watch([fullname, email, password], ([newFullname, newEmail, newPassword]) => {
  if (newFullname !== '' && newEmail !== '' && newPassword !== '') {
    isDisabled.value = false
    styleStates.disabledButton = ''
  } else {
    isDisabled.value = true
    styleStates.disabledButton = 'opacity-50'
  }
})

function inputStyle(style) {
  return `h-10 border ${style} rounded-md px-3 py-2 text-base focus:outline-none focus:px-4 focus:py-3`
}

const buttonStyle = computed(() => {
  return `w-full text-white b g-pink-700 ${styleStates.disabledButton} hover:bg-pink-800 focus:ring-4 focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-pink-600 dark:hover:bg-pink-700 focus:outline-none dark:focus:ring-pink-800`
})

// The API post request happens when the form is submitted
async function submitForm() {
  try {
    
    const payload = {
      fullname: fullname.value,
      email: email.value,
      password: password.value,
    }

    const res = await axios.post('http://localhost:8888/api/register', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    code.value = res.data.code

    if (code.value) {
      showAlert(isVisible)

      if (code.value === 404) {
        // show error alert
        type.value = 'error'
        message.value = 'Please, insert your data'
      } else {
        // show success alert
        type.value = 'success'
        message.value = 'Register success!'
      }
    }
  } catch (err) {
    console.error('Failed to fetch message:', err)
  }
}
</script>

<template>
  <!-- the submit event will no longer reload the page -->
  <form action="/register" method="post" @submit.prevent="submitForm">
    <div class="flex flex-col w-full gap-4">
      <div class="flex flex-col gap-2">
        <label for="fullname" class="text-sm font-medium text-neutral text-opacity-75">Full Name</label>
        <input v-model="fullname" autocomplete="off" placeholder="Enter your fullname" type="text"
          :class="inputStyle(styleStates.fullnameBorder)" />
      </div>
      <div class="flex flex-col gap-2">
        <label for="email" class="text-sm font-medium text-neutral text-opacity-75">Email</label>
        <input v-model="email" autocomplete="off" placeholder="Enter your email" type="text"
          :class="inputStyle(styleStates.emailBorder)" />
      </div>
      <div class="flex flex-col gap-2">
        <label for="password" class="text-sm font-medium text-neutral text-opacity-75">Password</label>
        <input v-model="password" autocomplete="off" placeholder="Enter your password" type="password"
          :class="inputStyle(styleStates.passwordBorder)" />
      </div>
      <button :disabled="isDisabled" type="submit" :class="buttonStyle">
        Create Account
      </button>
    </div>
  </form>
</template>
