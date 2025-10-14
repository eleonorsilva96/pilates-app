<script setup>
import ClassCard from '@/components/ClassCard.vue';
import api from '@/services/axios';
import { computed, onMounted, ref } from 'vue';

const classes = ref()
// let index = ref(0)

// make api request to get all classes
onMounted(async () => {
  try {
    const res = await api.get("/classes")

    classes.value = res.data.classes

    // console.log(classes.value)


  } catch(err) {

  }

})

// const increment_index = computed(() => {

//   for (let i = 0; i < classes.value.length + 1; i++) {

//     return index.value += 1

//   }
// })

// for (let i = 0; i < classes.value.length + 1; i++) {

//     // return index.value += 1
//     console.log(index.value)
//   }



</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex flex-col items-left mb-8">
      <h1 class="text-3xl font-bold text-foreground">Classes</h1>
      <p class="text-gray-600">Discover and book your next pilates session</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <RouterLink v-for="class_ in classes" :key="class_.class_.id" :to="{ name: 'class-detail', params: { slug: class_.class_.slug } }">
        <ClassCard :schedules_info="class_.schedules_info" :description="class_.class_.description"> {{ class_.class_.name }} </ClassCard>
      </RouterLink>
<!-- 
      <RouterLink v-for="class_ in classes" :key="class_['class_'].id" :to="{ name: 'class-detail', params: { slug: class_['class_'].slug } }">
        <ClassCard :schedules="class_['schedules']" :description="class_['class_'].description"> {{ class_['class_'].name }} </ClassCard>
      </RouterLink>
       -->
    </div>
  </div>
</template>

<style scoped>

</style>



<!-- <RouterLink v-for="class_ in classes" :key="class_.id" :to="{ name: 'class-detail', params: { slug: class_.slug } }">
        <ClassCard :description="class_.description"> {{ console.log(class_.name) }} </ClassCard>
      </RouterLink> -->