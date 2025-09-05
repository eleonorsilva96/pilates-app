<script setup>
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { ref, computed, onBeforeUnmount, onMounted, useTemplateRef } from 'vue'

const storeAuth = useAuthStore()
const { isAuthenticated, userInitials } = storeToRefs(storeAuth)

let showDrop = ref(false)
const dropdownRef = useTemplateRef('profile')

// computed variable
const combineInitials = computed(() => {
  return Object.values(userInitials.value).join("")
})

function handleClickOutside(e) {
  // checks if the clicked target is outside the profile dropdown
  if (showDrop.value && !dropdownRef.value.contains(e.target)) {
    showDrop.value = false
  }
}

// when component loads, a click event listener is added to the document
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

// then it is removed before the component unmounts
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

</script>

<template>
  <nav class="flex justify-between h-16">
    <RouterLink to="/" class="self-center font-bold text-xl">PilatesFlow</RouterLink>
    <div v-if="isAuthenticated" class="flex space-x-4 items-center">
      <div class="flex space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" class="text-black">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 2v4M16 2v4M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2M3 10h18"></path>
        </svg>
        <RouterLink to="/dashboard" class="font-medium text-neutral dark:text-neutral hover:underline">Dashboard
        </RouterLink>
      </div>
      <div class="flex space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" class="text-black">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 2v4M16 2v4M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2M3 10h18"></path>
        </svg>
        <RouterLink to="/classes" class="font-medium text-neutral dark:text-neutral hover:underline">Classes
        </RouterLink>
      </div>
      <div class="flex space-x-2 relative">
        <button class="font-medium text-neutral dark:text-neutral hover:no-underline" type="button" @click="showDrop = !showDrop" ref="profile">
          <div class="flex justify-center items-center rounded-full h-9 w-9 bg-pink-700">
            <span class="text-white">
              {{ combineInitials }}
            </span>
          </div>
        </button>
        <!-- Dropdown menu -->
        <div class="z-10 bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700 absolute top-10 right-0"
          v-show="showDrop">
          <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownDefaultButton">
            <li>
              <RouterLink to="/profile"
                class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Profile
              </RouterLink>
            </li>
            <li>
              <button type="button"
                class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white w-full text-left"
                @click="() => { storeAuth.logOut(); showDrop = false }">Log
                out</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-else class="flex space-x-4 items-center">
      <RouterLink to="/auth/login" class="font-medium text-neutral dark:text-neutral hover:underline">Login
      </RouterLink>
      <RouterLink to="/auth/register"
        class="text-white bg-pink-700 hover:bg-pink-800 focus:ring-4 focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-pink-600 dark:hover:bg-pink-700 focus:outline-none dark:focus:ring-pink-800">
        Get Started</RouterLink>
    </div>
  </nav>
</template>
