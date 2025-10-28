<script setup>
import Button from '@/components/Button.vue';
import ClassContainer from '@/components/ClassContainer.vue';
import api from '@/services/axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const class_details = ref()
const route = useRoute()

onMounted(async () => {
    try {
        const res = await api.get(`/classes/${route.params.slug}`)
        
        class_details.value = res.data.class_details

        // console.log(class_details.value.class_.name)

    } catch(err){

    }
})

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
            <h1 class="text-3xl font-bold text-foreground">{{ class_details?.class_.name }}</h1>
            <p class="text-gray-600">{{ class_details?.class_.description }}</p>
        </div>
        <!-- only pass object if it exists -->
        <div v-if="class_details" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ClassContainer :showForm="false" :schedules="class_details?.schedules">
                Class Information
            </ClassContainer>
            <ClassContainer :showForm="true" :schedules="class_details?.schedules" :dates="class_details?.dates">
                Book a Class
            </ClassContainer>
        </div>
    </div>
</template>