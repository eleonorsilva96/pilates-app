<script setup>
import { storeToRefs } from 'pinia'
import { useAlertsStore } from './stores/alerts'
import Alert from './components/Alert.vue'

const storeAlerts = useAlertsStore()

const { isVisible } = storeToRefs(storeAlerts)
</script>
<template>
  <!-- add header -->
  <div class="min-h-screen">
    <div class="border-b sticky">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <nav class="flex justify-between h-16">
          <RouterLink to="/" class="self-center font-bold text-xl">PilatesFlow</RouterLink>
          <div class="flex space-x-4 items-center">
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
      </div>
    </div>
    <main>
      <RouterView />
    </main>
    <Alert v-if="isVisible" />
  </div>
</template>

<style scoped></style>
