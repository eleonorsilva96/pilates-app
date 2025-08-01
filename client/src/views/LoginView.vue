<template>
  <form action="/login" method="post">
    <div class="flex flex-col w-full gap-4">
      <div class="flex flex-col gap-2">
        <label for="email" class="text-sm font-medium text-opacity-75">Email</label>
        <input
          autocomplete="off"
          name="email"
          placeholder="Enter your email"
          type="text"
          class="h-10 border rounded-md px-3 py-2 text-base focus:outline-none focus:border-2 focus:border-pink-400 focus:px-4 focus:py-3"
        />
      </div>
      <div class="flex flex-col gap-2">
        <label for="password" class="text-sm font-medium text-opacity-75">Password</label>
        <input
          autocomplete="off"
          name="password"
          placeholder="Enter your password"
          type="password"
          class="h-10 border rounded-md px-3 py-2 text-base focus:outline-none focus:border-2 focus:border-pink-400"
        />
      </div>
      <button
        class="w-full text-white bg-pink-700 hover:bg-pink-800 focus:ring-4 focus:ring-pink-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-pink-600 dark:hover:bg-pink-700 focus:outline-none dark:focus:ring-pink-800"
      >
        Login
      </button>
    </div>
  </form>
</template>
