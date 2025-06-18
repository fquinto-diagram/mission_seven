<template>
    <nav class="w-screen flex items-center justify-between bg-gradient-to-r from-purple-400 to-blue-500 pr-6 overflow-visible">
        <div class="flex items-center">
            <img src="@/assets/FQ_Logo.png" alt="Logo" class="w-20">
        </div>
        
        <div class="flex items-center">
            <ProfileMenu />
        </div>
    </nav>
</template>

<script setup lang="ts">
import ProfileMenu from '@/modules/common/components/ProfileMenu.vue';
</script>