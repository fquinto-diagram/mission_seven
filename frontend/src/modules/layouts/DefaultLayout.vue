<template>
    <div class="container w-screen h-screen min-h-screen bg-gradient-to-r from-purple-400 to-blue-500">
        <main class="container mx-auto">
            <img src="../../assets/FQ_Logo.png" class="justify-center">
            <MyNavBar />
            <MySideBar />
            <RouterView />
        </main>
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import MyNavBar from '@/modules/common/components/MyNavBar.vue';
import MySideBar from '@/modules/common/components/MyNavBar.vue';

</script>