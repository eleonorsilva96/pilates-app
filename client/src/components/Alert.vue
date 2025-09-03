<script setup>
import { capitalize } from '@/helpers/textHelpers'

const props = defineProps(['types', 'messages'])

const typeClasses = {
  error: 'text-red-800 bg-red-50',
  success: 'text-green-800 bg-green-50',
}
</script>
<template>
  <div class="fixed inset-x-0 bottom-0 mx-auto max-w-md">
    <div
      v-for="(value, index) in props.types"
      :key="index"
      :class="`p-4 mb-4 text-sm ${typeClasses[value]} rounded-lg`"
      role="alert"
    >
      <span class="font-medium">{{ capitalize(value) }} alert!</span> {{ messages[index] }}
    </div>
  </div>
</template>
