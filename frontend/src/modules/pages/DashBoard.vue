<template>
    <h1 class="mx-auto">Hola {{name}}, bienvenido a FqFacturación</h1>
</template>

<script setup lang="ts">
import { getUser } from '@/modules/auth/helpers/getUser';
import { useCookies } from 'vue3-cookies'
import { onMounted, ref } from 'vue';

const name = ref('')

const { cookies } = useCookies()
const token = cookies.get('token')

onMounted(async () => {
  if (!token) return 

  const response = await getUser(token)
  
  name.value = response?.data?.user.name ?? ''
})
</script>