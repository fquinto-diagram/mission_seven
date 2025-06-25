<template>
  <div class="p-4">
    <div v-if="!edit" class=" flex flex-wrap p-6 shadow-md items-center">
      <p class="text-lg m-2"><strong>Nombre:</strong> {{ user.name }}</p>
      <p class="text-lg m-2"><strong>Apellido:</strong> {{ user.surname }}</p>
      <p class="text-lg m-2"><strong>Email:</strong> {{ user.email }}</p>
      <p class="text-lg m-2"><strong>Lenguaje:</strong> {{ user.lang }}</p>
      <MyButton @click="handelEdit" text="Editar Perfil" class="mt-4 rounded-md p-2 bg-amber-300 text-white" />
    </div>

    <form v-else>
      <div class="flex flex-wrap gap-4 justify-between">
        <div class="flex flex-col w-full sm:w-[22%]">
          <label for="nombre" class="text-sm font-medium text-gray-700">Nombre</label>
          <MyInput v-model="user.name" id="nombre" placeholder="Nombre" class="mt-1" />
        </div>
        <div class="flex flex-col w-full sm:w-[22%]">
          <label for="apellido" class="text-sm font-medium text-gray-700">Apellido</label>
          <MyInput v-model="user.surname" id="apellido" placeholder="Apellido" class="mt-1" />
        </div>
        <div class="flex flex-col w-full sm:w-[25%]">
          <label for="email" class="text-sm font-medium text-gray-700">Email</label>
          <MyInput v-model="user.email" id="email" placeholder="Email" class="mt-1" />
        </div>
        <div class="flex flex-col w-full sm:w-[22%]">
          <label for="lang" class="text-sm font-medium text-gray-700">Lenguaje</label>
          <select v-model="user.lang" name="lang" class="m-2">
            <option v-for="lang in languages" :key="lang.id" :value="lang.id"> {{ lang.name }}</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end gap-2 mt-4">
        <MyButton @click="handelEdit" text="Cancelar" class="p-2 rounded-md bg-red-500 text-white" />
        <MyButton @click="handleSubmit" text="Enviar" class="p-2  rounded-md bg-blue-500 text-white" />
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useCookies } from 'vue3-cookies';
import MyInput from '@/modules/common/components/MyInput.vue';
import MyButton from '@/modules/common/components/MyButton.vue';
import { getUser } from '@/modules/auth/helpers/getUser';
import { putUser } from '@/modules/auth/helpers/putUser';
import type { User } from '@/modules/auth/interface/user.interface';
import { languages } from '@/modules/Profiles/interface/lang.interface';

const isLoaded = ref(false)
const edit = ref(false)
const { cookies } = useCookies()
const token = cookies.get('token')

const user = reactive<User>({
  name: '',
  surname: '',
  email: '',
  lang: '',
})

function handelEdit() {
  edit.value = !edit.value
}

async function handleSubmit() {
  if (!token) return;

  try {
    await putUser(token, user);
    alert("Usuario actualizado correctamente");
    edit.value = false;
  } catch (error) {
    alert("Error al actualizar el usuario");
  }
}

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