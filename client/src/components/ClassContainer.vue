<script setup>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { computed, onMounted, ref } from 'vue';
import { addComma, calculateDuration, convertDayWeek, convertMinutes, storeUniqueDaysWeek } from '@/helpers/generalHelpers';
import ButtonsCTA from './ButtonsCTA.vue';

// const props = defineProps(['showForm'])
const { showForm, classDetails, scheduleDetails, scheduleDates } = defineProps({
    showForm: Boolean,
    classDetails: Object,
    scheduleDetails: Object,
    scheduleDates: Array
})

const date = ref(new Date(scheduleDates?.[0])) // set to select only the first available day

const days_week_unique = ref([])
const teacher = ref('Not assigned')
let showTeacher = ref(false)
let isDisable = ref(true)
let selectedTime = ref(null)

// show only one day of week to avoid repeated days 
days_week_unique.value = storeUniqueDaysWeek(scheduleDetails.schedules)

// shift week day scale to 0=Monday ... 6=Sunday
const shiftWeekDay = computed(() => (date.value.getDay() + 6) % 7)

// return a new array with only the schedules whose day_of_week matches the selected day 
const schedulesForDay = computed(() => scheduleDetails.schedules.filter((schedule) => schedule.day_of_week === shiftWeekDay.value))

const setScheduleTime = (start_time) => {
    showTeacher.value = true
    selectedTime.value = start_time
    isDisable.value = false
    // find the schedule object with the class time to show the class teacher
    const timeSchedule = scheduleDetails.schedules.find((schedule) => schedule.start_time === start_time)
    teacher.value = timeSchedule.name
}

// change dynamically the bg color of the timer selector when click event happens
const isSelected = (start_time) => start_time === selectedTime.value

// when selected day changes
const handleDate = (modelData) => {
    selectedTime.value = null
    showTeacher.value = false
    isDisable.value = true
    // update the date to have the latest day_of_week
    date.value = modelData
}

</script>

<template>
    <div class="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
        <div class="flex flex-col gap-6">
            <h3 class="text-2xl font-semibold">
                <slot></slot>
            </h3>
            <!-- form -->
            <div v-if="showForm" class="flex gap-3">
                <!-- insert form element here -->
                <form action="">
                    <div class="flex flex-col gap-2">
                        <label for="" class="text-sm">Date</label>
                        <VueDatePicker v-model="date" :enable-time-picker="false" :allowed-dates="scheduleDates"
                            @update:model-value="handleDate" inline auto-apply />
                        <!-- <button type="button" class="flex items-center gap-2 border rounded-md bg-white p-3">
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
                              <span class="text-sm text-gray-500">Pick a Date</span>
                          </button> -->
                        <p class="text-sm text-gray-500">Only
                            <span v-for="(day_of_week, index) in days_week_unique" :key="index">
                                {{ addComma(index, convertDayWeek(day_of_week), days_week_unique) }}
                            </span>
                            are available for this class
                        </p>
                    </div>
                    <div class="flex flex-col gap-2 w-full">
                        <label for="times" class="text-sm">Time</label>
                        <div class="flex gap-2">
                            <div v-for="schedule in schedulesForDay" :key="schedule.id"
                                @click="setScheduleTime(schedule.start_time)" :class="['bg-white w-full border rounded-md p-3 cursor-pointer',
                                    isSelected(schedule.start_time) ? 'bg-pink-400' : 'hover:bg-pink-100',
                                ]">{{ schedule.start_time }}
                            </div>
                        </div>
                        <div v-if="showTeacher" class="flex gap-2 items-center">
                            <div class="flex gap-2 items-center">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round" class="lucide lucide-user w-4 h-4 text-gray-500"
                                    data-lov-id="src/pages/ClassesSimple.tsx:197:20" data-lov-name="User"
                                    data-component-path="src/pages/ClassesSimple.tsx" data-component-line="197"
                                    data-component-file="ClassesSimple.tsx" data-component-name="User"
                                    data-component-content="%7B%22className%22%3A%22w-4%20h-4%22%7D">
                                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                                    <circle cx="12" cy="7" r="4"></circle>
                                </svg>
                                <span class="text-sm font-medium">Instructor:</span>
                            </div>
                            <span class="text-base">{{ teacher }}</span>
                        </div>
                        <ButtonsCTA class="w-full mt-auto w-[96%] self-center" :is-disable="isDisable"
                            button-type="submit">Schedule Class</ButtonsCTA>
                        <!-- dropdown selector -->
                        <!-- <div class="relative inline-flex items-center bg-white h-12 w-full">
                              <select name="times" id="times" class="appearance-none absolute inset-0 w-full h-full border rounded-md p-3">
                                  <option value="8:00">8:00</option>
                                  <option value="8:00">8:00</option>
                                  <option value="8:00">8:00</option>
                              </select>
                         
                              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                  class="lucide lucide-chevron-down h-4 w-4 text-gray-500 absolute right-0 mr-3"
                                  data-lov-id="src/components/ui/select.tsx:27:6" data-lov-name="ChevronDown"
                                  data-component-path="src/components/ui/select.tsx" data-component-line="27"
                                  data-component-file="select.tsx" data-component-name="ChevronDown"
                                  data-component-content="%7B%22className%22%3A%22h-4%20w-4%20opacity-50%22%7D" aria-hidden="true">
                                  <path d="m6 9 6 6 6-6"></path>
                              </svg>
                          </div> -->
                    </div>
                </form>
            </div>
            <div v-else class="flex flex-col gap-3">
                <div class="flex gap-2 items-center">
                    <div class="flex gap-2 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="lucide lucide-user w-4 h-4 text-gray-500"
                            data-lov-id="src/pages/ClassesSimple.tsx:197:20" data-lov-name="User"
                            data-component-path="src/pages/ClassesSimple.tsx" data-component-line="197"
                            data-component-file="ClassesSimple.tsx" data-component-name="User"
                            data-component-content="%7B%22className%22%3A%22w-4%20h-4%22%7D">
                            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        <span class="text-sm font-medium">Instructors:</span>
                    </div>
                    <span v-for="(name, index) in scheduleDetails.sorted_names" :key="index" class="text-base">{{
                        addComma(index, name, scheduleDetails.sorted_names) }}</span>
                </div>
                <div class="flex gap-2 items-center">
                    <div class="flex gap-2 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="lucide lucide-calendar w-4 h-4 text-gray-500"
                            data-lov-id="src/pages/ClassDetail.tsx:200:16" data-lov-name="CalendarIcon"
                            data-component-path="src/pages/ClassDetail.tsx" data-component-line="200"
                            data-component-file="ClassDetail.tsx" data-component-name="CalendarIcon"
                            data-component-content="%7B%22className%22%3A%22w-4%20h-4%20mr-3%20text-muted-foreground%22%7D">
                            <path d="M8 2v4"></path>
                            <path d="M16 2v4"></path>
                            <rect width="18" height="18" x="3" y="4" rx="2"></rect>
                            <path d="M3 10h18"></path>
                        </svg>
                        <span class="text-sm font-medium">Days:</span>
                    </div>
                    <span v-for="(day_of_week, index) in days_week_unique" :key="index" class="text-base">
                        {{ addComma(index, convertDayWeek(day_of_week), days_week_unique) }}
                    </span>
                </div>
                <div class="flex gap-2 items-center">
                    <div class="flex gap-2 items-center">
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
                        <span class="text-sm font-medium">Times:</span>
                    </div>
                    <span v-for="(schedule, index) in scheduleDetails.schedules" :key="index" class="text-base">
                        {{ schedule.start_time }} - {{ schedule.end_time }} {{
                            addComma(index, calculateDuration(convertMinutes(schedule.start_time),
                                convertMinutes(schedule.end_time)), scheduleDetails.schedules) }}
                    </span>
                </div>
                <div class="flex gap-2 items-center">
                    <div class="flex gap-2 items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="lucide lucide-users w-4 h-4 text-gray-500"
                            data-lov-id="src/pages/ClassDetail.tsx:212:16" data-lov-name="Users"
                            data-component-path="src/pages/ClassDetail.tsx" data-component-line="212"
                            data-component-file="ClassDetail.tsx" data-component-name="Users"
                            data-component-content="%7B%22className%22%3A%22w-4%20h-4%20mr-3%20text-muted-foreground%22%7D">
                            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                            <circle cx="9" cy="7" r="4"></circle>
                            <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                        </svg>
                        <span class="text-sm font-medium">Available Spots</span>
                    </div>
                    <div
                        class="rounded-full border px-2.5 py-0.5 text-sm font-semibold transition-colors border-transparent top-3 right-3 bg-pink-200 bg-opacity-75">
                        <span><span>6</span> spots</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
