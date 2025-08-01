<script setup>

import { watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import login from './LoginView.vue'
import register from './RegisterView.vue'


const tabs = {
  login,
  register
}

const route = useRoute()

let currentTab = route.name

// let capitalizeCurrentTab = computed(() => 
//   currentTab.value ? currentTab.value.charAt(0).toUpperCase() + currentTab.value.slice(1) : ''
// )

function capitalize(word) {
  if (!word) return ''
  return word.charAt(0).toUpperCase() + word.slice(1)
}

console.log("load route " + currentTab)

// console.log("component login " + tabs['login'])

watch(() => route.name, (newRoute, oldRoute) => {
  // re-assign currentTab with new value
  console.log("new route " + newRoute)
  currentTab = newRoute
})


</script>

<template>
  <div class="container mx-auto px-4 max-w-md">
    <h1>Auth page</h1>
    <!-- tabs -->
     <div class="justify-evenly h-10 rounded-md bg-gray-200 text-muted-foreground p-1 flex flex-row">
      <RouterLink
      role="button"
      v-for="(_, tab) in tabs"
      :key="tab" 
      :class="['flex-auto', 'rounded-sm', 'px-3', 'py-1.5', 'text-sm', 'font-medium', 'transition-all', { active: currentTab === tab }]" 
      :to="`/auth/${tab}`"
      >
      {{ capitalize(tab) }}
    </RouterLink>
    <!-- </button> -->
      <!-- <button class="flex-auto rounded-sm px-3 py-1.5 text-sm font-medium transition-all">Register</button> -->
     </div>
    <RouterView></RouterView>
  </div>
</template>

<style scoped>

.active {
  background-color: white;
}

</style>
