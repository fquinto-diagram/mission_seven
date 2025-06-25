<template>
    <table class="table-auto bg-gray-100 border">
        <thead>
            <th class="border border-black px-4 py-2">ID</th>
            <th class="border border-black px-4 py-2">Nombre</th>
        </thead>
        <tbody v-for="rol in roles">
            <td class="border border-black px-4 py-2">{{ rol.id  }}</td>
            <td class="border border-black px-4 py-2">{{ rol.name }}</td>
        </tbody>
    </table>
</template>

<script setup lang="ts">
import { useListRoles } from '@/modules/roles/composables/useListRoles';

const { roles } = useListRoles() 

</script>