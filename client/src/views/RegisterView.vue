<script setup>
import { computed, reactive, ref, watch } from 'vue'
import axios from 'axios'
import { useAlertsStore } from '@/stores/alerts'
import { storeToRefs } from 'pinia'
import { showAlert } from '@/helpers/generalHelpers'
import { isValidEmail, isValidName } from '@/helpers/textHelpers'
import { useRouter } from 'vue-router'

const storeAlerts = useAlertsStore()
const { isVisible, type, message } = storeToRefs(storeAlerts)
const fullname = ref('')
const email = ref('')
const password = ref('')
let isDisabled = ref(true)
const router = useRouter()

const styleStates = reactive({
  fullnameBorder: 'focus:border-pink-400 focus:border-2',
  emailBorder: 'focus:border-pink-400 focus:border-2',
  passwordBorder: 'focus:border-pink-400 focus:border-2',
  disabledButton: 'opacity-50',
})

// I NEED TO CREATE AN INLINE ALERT FOR THE FIELD VALIDATIONS

// allow only letters in the name
// watch(fullname, (newVal) => {
//   if (newVal !== '' && !isValidName(newVal)) {
//     styleStates.fullnameBorder = 'border-red-500 border-2'
//     type.value.push('error')
//     message.value.push('Only letters are allowed in the name')
//     showAlert(isVisible, type, message)
//     } else {
//       styleStates.fullnameBorder = 'focus:border-pink-400 focus:border-2'
//     }
// })

// check for email format
// watch(email, (newVal) => {
//   if (newVal !== '' && !isValidEmail(newVal)) {
//     styleStates.emailBorder = 'border-red-500 border-2'
//     type.value.push('error')
//     message.value.push('Enter a valid email')
//     showAlert(isVisible, type, message)
//   } else {
//     styleStates.emailBorder = 'focus:border-pink-400 focus:border-2'
//   }
// })

// check if password is at least 5 characters
// watch(password, (newVal) => {
//   if (newVal !== '' && newVal.length < 5) {
//     styleStates.passwordBorder = 'border-red-500 border-2'
//     type.value.push('error')
//     message.value.push('Enter a password with at least 5 characters')
//     showAlert(isVisible, type, message)
//   } else {
//     styleStates.passwordBorder = 'focus:border-pink-400 focus:border-2'
//   }
// })

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
  // reset alerts store array to remove old values
  type.value = []
  message.value = []

  try {
    const payload = {
      fullname: fullname.value,
      email: email.value,
      password: password.value,
    }

    const res = await axios.post('http://localhost:8888/api/auth/register', payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // user created with success
    if (res.status === 201) {
      type.value.push('success')
      message.value.push(res.data.message)
      router.push('/auth/login')
      showAlert(isVisible, type, message)
    }
  } catch (err) {
    if (err.response) {
      // errors from the backend validations
      console.log(err.response.data.errors)

      err.response.data.errors.forEach((msg) => {
        type.value.push('error')
        message.value.push(msg)
        showAlert(isVisible, type, message)
      })
    } else {
      console.error('Failed to fetch message:', err)
    }
  }
}
</script>

<template>
  <!-- the submit event will no longer reload the page -->
  <form action="/register" method="post" @submit.prevent="submitForm">
    <div class="flex flex-col w-full gap-4">
      <div class="flex flex-col gap-2">
        <label for="fullname" class="text-sm font-medium text-neutral text-opacity-75"
          >Full Name</label
        >
        <input
          v-model="fullname"
          autocomplete="off"
          placeholder="Enter your fullname"
          type="text"
          :class="inputStyle(styleStates.fullnameBorder)"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="email" class="text-sm font-medium text-neutral text-opacity-75">Email</label>
        <input
          v-model="email"
          autocomplete="off"
          placeholder="Enter your email"
          type="text"
          :class="inputStyle(styleStates.emailBorder)"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="password" class="text-sm font-medium text-neutral text-opacity-75"
          >Password</label
        >
        <input
          v-model="password"
          autocomplete="off"
          placeholder="Enter your password"
          type="password"
          :class="inputStyle(styleStates.passwordBorder)"
        />
      </div>
      <button :disabled="isDisabled" type="submit" :class="buttonStyle">Create Account</button>
    </div>
  </form>
</template>
