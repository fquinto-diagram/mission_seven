<template>
    <nav class="w-screen flex items-center justify-between bg-gradient-to-r from-purple-400 to-blue-500 pr-4 pl-4 py-2 fixed top-0 left-0 z-50 h-20">
        <div class="flex items-center">
            <img src="@/assets/FQ_Logo.png" alt="Logo" style="cursor: pointer;" class="w-16 sm:w-20" @click="redirectDashboard()" />
        </div>
        <div class="flex items-center">
            <ProfileMenu />
        </div>
    </nav>
</template>

<script setup lang="ts">
import ProfileMenu from '@/modules/common/components/ProfileMenu.vue';
import { useRouter } from 'vue-router';

const router = useRouter()

function redirectDashboard() {
    router.push({name: 'dashboard'})
}
</script>