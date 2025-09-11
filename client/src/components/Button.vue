<script setup>

const props = defineProps(['path','text-color', 'bg-color', 'bg-color-hover', 'border-focus'])

</script>
<template>
    <RouterLink :to="props.path"
        :class="[props.textColor, props.bgColor, props.bgColorHover, props.borderFocus, 'w-[fit-content]', 'rounded-md', 'text-sm', 'font-medium', 'rounded-lg', 'border', 'text-base', 'px-5', 'py-3', 'focus:outline-none']">
        <slot></slot>
    </RouterLink>
</template>