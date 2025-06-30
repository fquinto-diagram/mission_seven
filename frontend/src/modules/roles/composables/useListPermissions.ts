import type { Permission } from '@/modules/roles/interfaces/permission.interface';
import { onMounted, ref } from 'vue';
import { useCookies } from 'vue3-cookies'
import { getAllPermissions } from '../../common/helpers/getPermission';

export function useListPermission() {
    const { cookies }= useCookies()
    const token = cookies.get('token')
    const permission = ref<Permission[]>([])

    onMounted(async ()=>{
        if (token){
            try{
                const response = await getAllPermissions()
                permission.value = response?.data ?? []
            }catch(error){
                alert(`Hay un error\n ${error}`)
            }
        }
    });
    return { permission }; 
}