<script setup>
import { computed, ref } from 'vue'
import { useAlertsStore } from '@/stores/alerts'
import { storeToRefs } from 'pinia'
import { capitalize } from '@/helpers/textHelpers'

const storeAlerts = useAlertsStore()

const { type, message } = storeToRefs(storeAlerts)

const typeClasses = {
  error: 'text-red-800 bg-red-50',
  success: 'text-green-800 bg-green-50',
}

const alertColor = computed(() => {
  return `p-4 mb-8 text-sm ${typeClasses[type.value]} rounded-lg`
})
</script>
<template>
  <div class="fixed inset-x-0 bottom-0 mx-auto max-w-md">
    <div :class="alertColor" role="alert">
      <span class="font-medium">{{ capitalize(type) }} alert!</span> {{ message }}
    </div>
  </div>
</template>
