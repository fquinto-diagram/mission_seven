<template>
  <form @submit.prevent="handleSubmit" class="grid bg-gray-200  py-4 px-4 my-4 w-auto">
    <strong class="mx-auto my-2 text-2xl">
      Nombre del rol</strong>
      <input v-model="rol.name" type="text" class="mx-auto bg-white rounded-md m-2 p-2" required />

    <div class="text-black m-2">
      <label v-for="perm in permissions" :key="perm.id" class="grid grid-flow-col items-center">
        <input type="checkbox":value="perm.id" v-model="rol.permissions"/>
        {{ perm.name }}
      </label>
    </div>

    <button type="submit" class="m-2 bg-white mx-auto p-2 rounded-md shadow-md">Guardar cambios</button>
  </form>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { putRol } from '@/modules/roles/helpers/putRoles'
import type { Rol } from '@/modules/roles/interfaces/role.interface'
import { getAllPermissions } from '@/modules/common/helpers/getPermission'
import { getRolById } from '@/modules/roles/helpers/getRolById' 
import type { Permission } from '../interfaces/permission.interface'

const route = useRoute()
const router = useRouter()
const permissions = ref<Permission[]>([])
const rol = reactive<Rol>({
  name: '',
  permissions: []
})


onMounted(async () => {
  const perms = await getAllPermissions()
  console.log('Permisos recibidos:', perms)   
  permissions.value = perms?.data ?? []

  const id = Number(route.params.id)
  if (!id) {
    alert('ID de rol no válida')
    router.push({ name: 'roles-list' })
    return
  }

  const data = await getRolById(id)
  console.log('in:', data)
  const roleData = Array.isArray(data) ? data[0]?.role : data.role
  rol.name = roleData?.name ?? ''
  rol.permissions = Array.isArray(roleData?.permissions)
    ? roleData.permissions.map((p: any) => typeof p === 'object' ? p.id : p)
    : []
})

async function handleSubmit() {
  const id = Number(route.params.id)
  try {
    await putRol(id, {
      name: rol.name,
      permissions: rol.permissions
    })
    alert('Rol actualizado correctamente')
    router.push({ name: 'roles-list' })
  } catch (error) {
    alert('Error al actualizar el rol')
  }
}
</script>