<template>
    <input :placeholder="placeholder" :type="type" :required="required" class="rounded-2xl p-2" :value="modelValue" @input="updateValue($event)">
</template>

<script setup lang="ts">
import type{ Input } from '@/modules/common/interface/input.interface'

defineProps<Input>()
const emit= defineEmits<{
    (e: 'update:modelValue', value: string): void
}>()

function updateValue(event: Event) {
    const target = event.target as HTMLInputElement
    emit('update:modelValue', target.value)
}

</script>