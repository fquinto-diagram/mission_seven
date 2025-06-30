<template>
    <h1 class="mx-auto">Hola {{ user.name }}, bienvenido a FqFacturación</h1>
</template>

<script setup lang="ts">
import { getUser } from '@/modules/profiles/helpers/getUser';
import { useCookies } from 'vue3-cookies'
import { onMounted, reactive } from 'vue';
import type { User } from '@/modules/auth/interface/user.interface';

const user = reactive<User>({
  name: '',
  surname: '',
  email: '',
  lang: '',
})

const { cookies } = useCookies()
const token = cookies.get('token')

onMounted(async () => {
  if (token) {
    try {
      const response = await getUser()
      if (response && 'user' in response) {
        Object.assign(user, response.user)
      } else {
        console.warn('Usuario no encontrado o formato inesperado')
      }
    } catch (error) {
      console.error('Error al obtener usuario:', error)
    }
  }
})
</script>