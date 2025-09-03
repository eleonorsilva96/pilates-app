<script setup>
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const storeAuth = useAuthStore()
const { isAuthenticated } = storeToRefs(storeAuth)
</script>

<template>
  <nav class="flex justify-between h-16">
    <RouterLink to="/" class="self-center font-bold text-xl">PilatesFlow</RouterLink>
    <div v-if="isAuthenticated" class="flex space-x-4 items-center">
      <div class="flex space-x-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          fill="none"
          class="text-black"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 2v4M16 2v4M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2M3 10h18"
          ></path>
        </svg>
        <RouterLink
          to="/dashboard"
          class="font-medium text-neutral dark:text-neutral hover:underline"
          >Dashboard
        </RouterLink>
      </div>
      <div class="flex space-x-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          fill="none"
          class="text-black"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 2v4M16 2v4M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2M3 10h18"
          ></path>
        </svg>
        <RouterLink to="/classes" class="font-medium text-neutral dark:text-neutral hover:underline"
          >Classes
        </RouterLink>
      </div>
    </div>
    <div v-else class="flex space-x-4 items-center">
      <RouterLink
        to="/auth/login"
        class="font-medium text-neutral dark:text-neutral hover:underline"
        >Login
      </RouterLink>
      <RouterLink
        to="/auth/register"
        class="text-white bg-pink-700 hover:bg-pink-800 focus:ring-4 focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-pink-600 dark:hover:bg-pink-700 focus:outline-none dark:focus:ring-pink-800"
      >
        Get Started</RouterLink
      >
    </div>
  </nav>
</template>
