<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref('')

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8888/api/hello')
    message.value = res.data.message
  } catch (err) {
    console.error('Failed to fetch message:', err)
  }
})
</script>

<template>
  <!-- add header -->
  <div class="min-h-screen">
    <div class="border-b sticky">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <nav class="flex justify-between h-16">
          <a href="" class="self-center"><span class="font-bold text-xl">PilatesFlow</span></a>
          <div class="flex space-x-4 items-center">
            <a href="" class="font-medium text-pink-600 dark:text-pink-500 hover:underline">Login</a>
            <a href="" class="text-white bg-pink-700 hover:bg-pink-800 focus:ring-4 focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-pink-600 dark:hover:bg-pink-700 focus:outline-none dark:focus:ring-pink-800">Get Started</a>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
