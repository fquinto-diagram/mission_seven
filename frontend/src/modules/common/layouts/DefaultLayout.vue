<template>
  <div class="bg-white">
    <MyNavBar />
    <MySideBar />
    <main class="flex justify-center transition-all duration-300 pt-20 pl-16 md:pl-[180px] md:mt-15 p-2 md:p-6 ">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import MyNavBar from '@/modules/common/components/MyNavBar.vue';
import MySideBar from '@/modules/common/components/MySideBar.vue';
</script>