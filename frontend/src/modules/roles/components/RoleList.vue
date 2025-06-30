<template>
    <div class="flex flex-col justify-center">
        <MyButton @click="redirectNew" text="Nuevo rol" class="bg-gradient-to-r from-purple-400 to-blue-500 text-white px-4 py-2 rounded-md mx-auto my-4" />
        <table class="table-auto">
            <thead class="bg-gray-300 border">
                <th class="border px-4 py-2">Nombre</th>
                <th class="border  px-4 py-2">Acciones</th>
            </thead>
            <tbody v-for="rol in roles" class="bg-gray-100 border">
                <td class="border px-4 py-2 capitalize">{{ rol.name }}</td>
                <td>
                    <MyButton @click="router.push({ name: 'roles-edit', params: { id: rol.id } })" :key="rol.id" text="Editar" class="m-2 p-2 rounded-md text-white bg-amber-500" />
                    <MyButton @click="confirmDelete(rol.id)" text="Eliminar" class="m-2 p-2 rounded-md text-white bg-red-500" />
                </td>
            </tbody>
        </table>
        <div class="flex my-4">
                <MyButton @click="prevPage" text="Anterior" class="bg-gradient-to-r from-purple-400 to-blue-500 text-white px-4 py-2 rounded-md mx-auto my-4"/>
                <span class="px-4 py-2 my-4">Página {{ page }}</span>
                <MyButton @click="nextPage" text="Siguiente" class="bg-gradient-to-r from-purple-400 to-blue-500 text-white px-4 py-2 rounded-md mx-auto my-4" />
            </div>
    </div>
    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black/15">
        <div class="bg-white p-6 rounded shadow-md">
            <p>¿Seguro que quieres eliminar este rol?</p>
            <div class="flex justify-end gap-2 mt-4">
            <MyButton text="Atras" @click="showModal = false" class="px-4 py-2 bg-gray-300 rounded" />
            <MyButton text="Eliminar" @click="handleDelete" class="px-4 py-2 bg-red-500 text-white rounded" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import MyButton from '@/modules/common/components/MyButton.vue';
import { deleteRol } from '@/modules/roles/helpers/deleteRoles';
import { useListRoles } from '@/modules/roles/composables/useListRoles';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const { roles, page, nextPage, prevPage, fetchRoles } = useListRoles()
const router = useRouter()

const showModal = ref(false)
const rolToDelete = ref<number | undefined>(undefined)

function confirmDelete(id: number | undefined) {
  rolToDelete.value = id
  showModal.value = true
}

async function handleDelete() {
  if (rolToDelete.value !== undefined) {
    await deleteRol(rolToDelete.value)
    fetchRoles()
    showModal.value = false
    rolToDelete.value = undefined
  }
}

function redirectNew(){
    router.push({ name: 'roles-form'})    
}
</script>