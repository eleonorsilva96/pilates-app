<!-- adjust it, use only the button -->

<script setup>
const props = defineProps(['is-single-btn'])
</script>
<template>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <button
      class="text-white bg-pink-700 hover:bg-pink-800 focus:ring-4 focus:ring-pink-300 font-medium rounded-lg text-base px-5 py-3 dark:bg-pink-600 dark:hover:bg-pink-700 focus:outline-none dark:focus:ring-pink-800"
    >
      Start your Jouney
    </button>
    <button
      v-if="!props.isSingleBtn"
      type="button"
      class="text-pink-700 hover:text-white bg-white border border-pink-700 hover:bg-pink-800 focus:ring-4 focus:outline-none focus:ring-pink-300 font-medium rounded-lg text-base px-5 py-3 text-center dark:border-pink-500 dark:text-pink-500 dark:hover:text-white dark:hover:bg-pink-500 dark:focus:ring-pink-800"
    >
      Meet Our Classes
    </button>
  </div>
</template>
