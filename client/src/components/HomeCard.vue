<script setup>
const props = defineProps({
  icon: Object,
})
</script>

<template>
  <div class="rounded-lg bg-card flex flex-col items-center border-0 shadow-lg p-5 bg-white gap-4">
    <div class="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center bg-pink-100">
      <component :is="props.icon" class="text-pink-700" />
    </div>
    <h3 class="font-semibold text-xl">Flexible Scheduling</h3>
    <p class="text-base text-center">
      Book classes that fit your schedule with our easy-to-use booking system. Available 7 days a
      week with multiple time slots.
    </p>
  </div>
</template>
