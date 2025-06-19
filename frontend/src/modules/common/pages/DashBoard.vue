<template>
    <div class="ml-64">
        <div>
            <h1>Texto de Ejemplo</h1>
            <MyButton @click="getUser()" class="bg-black" text="Holaaaa"/>
        </div>
    </div>
</template>

<script setup lang="ts">
import MyButton from '@/modules/common/components/MyButton.vue';
import { getUser } from '@/modules/auth/helpers/getUser';
</script>