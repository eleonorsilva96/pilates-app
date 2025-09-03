<script setup>
import { storeToRefs } from 'pinia'
import { useAlertsStore } from './stores/alerts'
import { useAuthStore } from './stores/auth'
import Alert from './components/Alert.vue'
import Header from './components/Header.vue'
import { onMounted } from 'vue'
import { watch } from 'vue'

const storeAlerts = useAlertsStore()

const { isVisible, type, message } = storeToRefs(storeAlerts)

onMounted(async () => {
  const storeAuth = useAuthStore()
  // check if user is authenticated to ensure the auth store global variable is synced with backend
  // if happens full page loads or close pages the token still persists because is stored in a http-only cookie
  storeAuth.initAuth()
})
</script>
<template>
  <!-- add header -->
  <div class="min-h-screen">
    <div class="border-b sticky">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <Header />
      </div>
    </div>
    <main>
      <RouterView />
    </main>
    <Alert v-if="isVisible" :types="type" :messages="message" />
  </div>
</template>

<style scoped></style>
