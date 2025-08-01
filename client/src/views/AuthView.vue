<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import login from './LoginView.vue'
import register from './RegisterView.vue'

const tabs = {
  login,
  register,
}

const route = useRoute()

let currentTab = ref(route.name)

function capitalize(word) {
  if (!word) return ''
  return word.charAt(0).toUpperCase() + word.slice(1)
}

watch(
  () => route.name,
  (newRoute, oldRoute) => {
    // re-assign currentTab with new value
    console.log('new route ' + newRoute)
    currentTab = newRoute
  },
)
</script>

<template>
  <div class="h-screen flex items-center">
    <div
      class="flex flex-col gap-6 container mx-auto px-6 py-6 max-w-md border border-gray-300 rounded-lg"
    >
      <div class="flex flex-col items-center">
        <h3 class="text-2xl font-bold">Welcome to PilatesFlow</h3>
        <p class="text-sm text-gray-400 pt-2">Join our community of pilates enthusiasts</p>
      </div>
      <!-- tab navigation and form -->
      <div class="flex flex-col gap-3">
        <div class="justify-evenly h-10 rounded-md bg-brand-muted p-1 flex flex-row">
          <RouterLink
            role="button"
            v-for="(_, tab) in tabs"
            :key="tab"
            :class="[
              'flex-auto',
              'rounded-sm',
              'px-3',
              'py-1.5',
              'text-sm',
              'font-medium',
              'transition-all',
              'text-center',
              'text-brand-dark',
              {
                'shadow-sm': currentTab === tab,
                'text-neutral': currentTab === tab,
                active: currentTab === tab,
              },
            ]"
            :to="`/auth/${tab}`"
          >
            {{ capitalize(tab) }}
          </RouterLink>
        </div>
        <RouterView></RouterView>
      </div>
    </div>
  </div>
</template>

<style scoped>
.active {
  background-color: white;
}
</style>
