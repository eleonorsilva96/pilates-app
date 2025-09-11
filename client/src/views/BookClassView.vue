<script setup>
import Button from '@/components/Button.vue';
import ClassContainer from '@/components/ClassContainer.vue';
</script>

<template>
    <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col items-left mb-8 gap-2">
            <Button 
            path="/classes"
            text-color="text-black"
            bg-color="bg-white"
            bg-color-hover="hover:bg-pink-300"
            border-focus="focus:ring-4 focus:ring-pink-300"
            >
            Back to Classes
            </Button>
            <h1 class="text-3xl font-bold text-foreground">Pilates Matt</h1>
            <p class="text-gray-600">Energizing morning pilates class to start your day</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ClassContainer :show-form="false">
                Class Information
            </ClassContainer>
            <ClassContainer :show-form="true">
                Book a Class
            </ClassContainer>
        </div>
    </div>
</template>