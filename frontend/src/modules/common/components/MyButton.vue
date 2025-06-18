<template>
    <button :type="type" @click="$emit('click')" class="bg-white text-black p-2 rounded-2xl">{{ text }}</button>
</template>

<script setup lang="ts">
import type { Button } from '@/modules/common/interface/button.interface'

defineProps<Button>()

defineEmits(['click'])
</script>
<style scoped>

</style>