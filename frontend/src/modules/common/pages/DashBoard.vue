<template>
    <div class="ml-64">
        <div>
            <h1 class="bg">Texto de Ejemplo</h1>
        </div>
        <MyButton style="cursor: pointer;" class="bg-amber-300 text-amber-300" text="Holaaaa" @click="console.log(getUser())" />
    </div>
</template>

<script setup lang="ts">
import MyButton from '@/modules/common/components/MyButton.vue';
import { getUser } from '@/modules/auth/helpers/getUser';



</script>