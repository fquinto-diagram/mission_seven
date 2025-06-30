<template>
    <form @submit.prevent="handleSubmit" class="grid bg-gray-200  py-4 px-4 my-4 w-auto">
        <strong class="mx-auto my-2 text-2xl">Nombre</strong>
        <MyInput v-model="rol.name" id="name" placeholder="Nombre" class="mx-auto bg-white rounded-md"/>
        <template v-for="per in permission" :key="per.id">
            <div class="grid grid-flow-col items-center">
                <span>{{ per.name }}</span>
                <input type="checkbox" :value="per.id" v-model="rol.permissions" class="justify-center" />
            </div>
        </template>
        <MyButton text="Enviar" class="bg-white rounded-md mx-auto mt-2 p-2"/>
    </form>
</template>
    
<script setup lang="ts">
import MyButton from '@/modules/common/components/MyButton.vue';
import MyInput from '@/modules/common/components/MyInput.vue';
import { useListPermission } from '../composables/useListPermissions';
import { postRoles } from '@/modules/roles/helpers/postRoles';
import type { Rol } from '../interfaces/role.interface';
import { reactive } from 'vue';
import { useCookies } from 'vue3-cookies'
import { useRouter } from 'vue-router';

const router = useRouter()
const { cookies }= useCookies()
const token = cookies.get('token') 
const { permission }= useListPermission()
const rol = reactive<Rol>({
    name: '',
    permissions: []
})

async function handleSubmit() {
    if (!token) return;
    try {
        await postRoles(rol);
        alert("Usuario actualizado correctamente");
    } catch (error) {
        alert("Error al actualizar el usuario");
    }finally{
        router.push({ name: 'roles-list'})
    }
}

</script>