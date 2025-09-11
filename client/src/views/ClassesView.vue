<script setup>
import ClassCard from '@/components/ClassCard.vue';


</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex flex-col items-left mb-8">
      <h1 class="text-3xl font-bold text-foreground">Classes</h1>
      <p class="text-gray-600">Discover and book your next pilates session</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <RouterLink to="/classes/book-class">
        <ClassCard />
      </RouterLink>
      <ClassCard />
      <ClassCard />
    </div>
  </div>
</template>

<style scoped>

</style>
