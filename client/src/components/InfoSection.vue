<script setup>
import IconCalendar from '@/assets/calendar.svg'
import IconPeople from '@/assets/people.svg'
import HomeCard from './HomeCard.vue'
import ButtonsCTA from './ButtonsCTA.vue'

const props = defineProps(['bg-pink', 'title', 'description', 'is-card', 'is-single-btn'])
</script>

<template>
  <section :class="['py-20', props.bgPink]">
    <div class="container mx-auto px-4">
      <div class="flex flex-col gap-8 align items-center">
        <h1 class="text-5xl md:text-6xl font-bold max-w-2xl text-center">{{ props.title }}</h1>
        <p class="text-xl text-gray-500 text-lg max-w-2xl text-center">{{ props.description }}</p>
        <!-- HomeCard or ButtonsCTA -->
        <div v-if="props.isCard" class="flex flex-col lg:flex-row items-strech gap-8">
          <HomeCard :icon="IconCalendar" />
          <HomeCard :icon="IconPeople" />
          <HomeCard :icon="IconCalendar" />
        </div>
        <ButtonsCTA v-else :is-single-btn="props.isSingleBtn" />
      </div>
    </div>
  </section>
</template>

<style scoped></style>
