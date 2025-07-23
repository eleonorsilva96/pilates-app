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
  <h1>{{ message }}</h1>
</template>

<style scoped></style>
