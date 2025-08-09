import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAlertsStore = defineStore('alerts', () => {
  let isVisible = ref(false)
  let type = ref([])
  let message = ref([])

  return { isVisible, type, message }
})
