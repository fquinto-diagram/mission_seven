import { getRoles } from '@/modules/roles/helpers/getRoles';
import type { Role } from '@/modules/roles/interfaces/role.interface';
import { onMounted, ref } from 'vue';
import { useCookies } from 'vue3-cookies'

export function useListRoles() {
    const { cookies }= useCookies()
    const token = cookies.get('token')
    const roles = ref<Role[]>([])

    onMounted(async ()=>{
        if (token){
            try{
                const response = await getRoles()
                console.log(response);
                roles.value = response?.data ?? []
            }catch(error){
                alert(`Hay un error\n ${error}`)
            }
        }
    });
    return { roles }; 
}