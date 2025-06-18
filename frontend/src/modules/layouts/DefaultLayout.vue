<template>
    <div class="container w-screen h-screen min-h-screen bg-white">
        <main class="container mx-auto">
            <MyNavBar />
            <MySideBar />
            <RouterView  class=""/>
        </main>
    </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import MyNavBar from '@/modules/common/components/MyNavBar.vue';
import MySideBar from '@/modules/common/components/MySideBar.vue';

</script>