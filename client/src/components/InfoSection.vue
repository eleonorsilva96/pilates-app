<script setup>
import HomeCard from './HomeCard.vue';
import ButtonsCTA from './ButtonsCTA.vue';

const props = defineProps(['bg-pink', 'title', 'description', 'is-card'])
// const props = defineProps({
//     title: String,
//     description: String,
//     isCard: Boolean
// })

</script>

<template>
    <div :class="['container', 'mx-auto', 'px-4', 'py-20', props.bgPink]">
        <div class="flex flex-col gap-8 align items-center">
            <h1 class="text-5xl md:text-6xl font-bold max-w-2xl text-center">{{ props.title }}</h1>
            <p class="text-xl text-gray-500 text-lg max-w-2xl text-center">{{ props.description }}</p>
            <!-- HomeCard or ButtonsCTA -->
             <HomeCard v-if="props.isCard"/>
             <ButtonsCTA v-else/>
        </div>
    </div>
</template>

<style scoped></style>