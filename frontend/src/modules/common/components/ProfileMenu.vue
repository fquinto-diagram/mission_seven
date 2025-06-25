<template>
    <div class="felx flex-col justify-end relative">
        <span class="flex items-center bg-gray-100 p-2 rounded-md" @click="isMenu = !isMenu" style="cursor:pointer"> 
            <svg xmlns="http://www.w3.org/2000/svg" width="2em" height="1em" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 4a4 4 0 0 1 4 4a4 4 0 0 1-4 4a4 4 0 0 1-4-4a4 4 0 0 1 4-4m0 10c4.42 0 8 1.79 8 4v2H4v-2c0-2.21 3.58-4 8-4Z"/>
            </svg>
            <p class="pr-2">{{ user.name }}</p>
        </span>
        <div v-if="isMenu" class="bg-gray-100 mr-auto p-2 mt-2 rounded-md absolute justify-items-end">
            <MyButton class="bg-gray-200 hover:gray-200" @click="handleLogout" text="Cerrar Sessión"/>
        </div>
    </div>
</template>

<script setup lang="ts">
import { getUser } from '@/modules/auth/helpers/getUser';
import { useAuthStore } from '@/modules/auth/store/storeCredentials';
import { useRouter } from 'vue-router';
import { onMounted, ref, reactive } from 'vue';
import { useCookies } from 'vue3-cookies'
import MyButton from './MyButton.vue';
import type { User } from '@/modules/auth/interface/user.interface';

const isMenu = ref(false)
const { cookies } = useCookies()
const token = cookies.get('token')
const store = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  store.logOut()
  router.push({name: 'login-form'})
}

const user = reactive<User>({
  name: '',
  surname: '',
  email: '',
  lang: '',
})

onMounted(async () => {
  if (token) {
    try {
      const response = await getUser(token)

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