<script setup>
import InfoSection from '../components/InfoSection.vue'
import HomeCard from '../components/HomeCard.vue'
</script>

<template>
  <div class="min-h-screen bg-white">
    <InfoSection bg-pink="bg-pink-100" title="Transform Your Body with
                PilatesFlow" description="Join our community of pilates enthusiasts and
                discover the perfect balance of strength, flexibility, and mindfulness with our expert instructors." 
                :is-card="false" :is-single-btn="false"/>
    <InfoSection title="Transform Your Body with
                PilatesFlow" description="Join our community of pilates enthusiasts and
                discover the perfect balance of strength, flexibility, and mindfulness with our expert instructors." 
                :is-card="true" :is-single-btn="false"/>
    <InfoSection bg-pink="bg-pink-100" title="Transform Your Body with
                PilatesFlow" description="Join our community of pilates enthusiasts and
                discover the perfect balance of strength, flexibility, and mindfulness with our expert instructors." 
                :is-card="false" :is-single-btn="true"/>
  </div>
</template>
