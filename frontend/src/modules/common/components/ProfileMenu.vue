<template>
    <div class="felx flex-col justify-end relative">
        <span class="flex items-center bg-gray-100 p-2 rounded-md" @click="isMenu = !isMenu" style="cursor:pointer"> 
            <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="1em" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 4a4 4 0 0 1 4 4a4 4 0 0 1-4 4a4 4 0 0 1-4-4a4 4 0 0 1 4-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4Z"/>
            </svg>
            <p class="pr-2">{{ isMenu }}</p>
        </span>
        <div v-if="isMenu" class="bg-gray-100 mr-auto p-2 mt-2 rounded-md absolute justify-items-end">
            <router-link v-for="route in routes" :to="{ name: route.name}">

            </router-link>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const isMenu = ref(false)

const routes = [
    {
        name: 'login'
    }
]
</script>