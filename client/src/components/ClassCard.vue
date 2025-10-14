<script setup>
import { ref } from 'vue';
import { convertDayWeekShortName, storeUniqueDaysWeek, addComma } from '@/helpers/generalHelpers';

// destructure props object 
const { description, schedules_info } = defineProps({
    description: String,
    schedules_info: Object
})

const days_week_filtered = ref([])

days_week_filtered.value = storeUniqueDaysWeek(schedules_info.schedules)

console.log(days_week_filtered.value)

</script>

<template>
    <div
        class="flex flex-col rounded-lg bg-card text-card-foreground shadow-sm group cursor-pointer overflow-hidden hover-scale transition-all duration-300 hover:shadow-xl border bg-gradient-to-br from-background">
        <div class="relative h-48 overflow-hidden">
            <img src="../assets/pilates_matt.jpg" alt="Pilates Matt Girl"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                :style="{ objectPosition: '0 88%' }">
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
            <div
                class="rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors border-transparent absolute top-3 right-3 bg-white bg-opacity-75">
                <span><span>6</span> spots</span>
            </div>
        </div>
        <div class="flex flex-col items-start p-4 gap-2">
            <div class="flex flex-col gap-1 w-full">
                <h3
                    class="font-semibold tracking-tight text-xl group-hover:text-primary transition-colors duration-200">
                    <slot></slot>
                </h3>
                <p class="text-sm text-gray-600">{{ description }}</p>
            </div>
            <div class="flex justify-between gap-2 w-full">
                <div class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-clock w-4 h-4 text-gray-500"
                        data-lov-id="src/pages/ClassesSimple.tsx:186:20" data-lov-name="Clock"
                        data-component-path="src/pages/ClassesSimple.tsx" data-component-line="186"
                        data-component-file="ClassesSimple.tsx" data-component-name="Clock"
                        data-component-content="%7B%22className%22%3A%22w-4%20h-4%22%7D">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                    <div class="flex gap-2">
                        <!-- class occurrences -->
                        <span v-for="(schedule, index) in schedules_info.schedules" :key="index" class="text-gray-500 text-sm">{{
                            schedule.start_time }}</span>
                    </div>
                </div>
                <div class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                        class="lucide lucide-calendar w-4 h-4 text-gray-500"
                        data-lov-id="src/pages/ClassesSimple.tsx:190:20" data-lov-name="Calendar"
                        data-component-path="src/pages/ClassesSimple.tsx" data-component-line="190"
                        data-component-file="ClassesSimple.tsx" data-component-name="Calendar"
                        data-component-content="%7B%22className%22%3A%22w-4%20h-4%22%7D">
                        <path d="M8 2v4"></path>
                        <path d="M16 2v4"></path>
                        <rect width="18" height="18" x="3" y="4" rx="2"></rect>
                        <path d="M3 10h18"></path>
                    </svg>
                    <span v-for="(day_of_week, index) in days_week_filtered" :key="index" class="text-gray-500 text-sm">{{
                        addComma(index, convertDayWeekShortName(day_of_week), days_week_filtered) }}</span>
                </div>
            </div>
            <div class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="lucide lucide-user w-4 h-4 text-gray-500" data-lov-id="src/pages/ClassesSimple.tsx:197:20"
                    data-lov-name="User" data-component-path="src/pages/ClassesSimple.tsx" data-component-line="197"
                    data-component-file="ClassesSimple.tsx" data-component-name="User"
                    data-component-content="%7B%22className%22%3A%22w-4%20h-4%22%7D">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <span v-for="(name, index) in schedules_info.sorted_names" :key="index" class="text-gray-500 text-sm">{{ addComma(index, name, schedules_info.sorted_names) }}</span>
            </div>
        </div>
    </div>
</template>

<!-- index != schedules.length - 1 ? schedule.name + ',' : schedule.name  -->