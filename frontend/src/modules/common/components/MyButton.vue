<template>
    <button :type="type" @click="$emit('click')" class="text-black">{{ text }}</button>
</template>

<script setup lang="ts">
import type { Button } from '@/modules/common/interface/button.interface'

defineProps<Button>()

defineEmits(['click'])
</script>
<style scoped>

</style>