import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAlertsStore = defineStore('alerts', () => {
  let isVisible = ref(false)
  let type = ref('error')
  let message = ref('Something went wrong!')

  return { isVisible, type, message }
})
