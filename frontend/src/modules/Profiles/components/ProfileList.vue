<template>
    <form class="bg-gray-100 flex flex-col justify-center">
        <MyInput :placeholder="user.name" />
        <MyButton text="Enviar" />
    </form>
</template>

<script setup lang="ts">
import MyInput from '@/modules/common/components/MyInput.vue';
import MyButton from '@/modules/common/components/MyButton.vue';
import { getUser } from '@/modules/auth/helpers/getUser';
import type { User } from '@/modules/auth/interface/user.interface';
import { useCookies } from 'vue3-cookies'
import {ref, reactive, onMounted} from 'vue'


const { cookies } = useCookies()
const token = cookies.get('token')
const user = reactive<User>({
  name: '',
  surname: '',
  email: '',
  lang: '',
})

const isLoaded = ref(false)

onMounted(async () => {
  if (token) {
    try {
      const response = await getUser(token)

      if (response && 'user' in response) {
        Object.assign(user, response.user)
        isLoaded.value = true
      } else {
        console.warn('Usuario no encontrado o formato inesperado')
      }
    } catch (error) {
      console.error('Error al obtener usuario:', error)
    }
  }
})


</script>