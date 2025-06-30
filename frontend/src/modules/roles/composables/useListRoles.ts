import { getAllRoles } from '@/modules/roles/helpers/getRoles';
import type { Rol } from '@/modules/roles/interfaces/role.interface';
import { ref, watch } from 'vue';

export function useListRoles() {

    const roles = ref<Rol[]>([])
    const page = ref(1)
    const totalPages = ref(1)

    async function fetchRoles() {
        const data = await getAllRoles(page.value)
        roles.value = data?.data || []
        totalPages.value = data?.total_pages || 1
    }

    function nextPage(){
        page.value ++
        fetchRoles()
        if (page.value > totalPages.value){
            page.value = totalPages.value
        }
    }
    
    function prevPage(){
        if (page.value > 1){
            page.value -- 
            fetchRoles()
        }
    }

    fetchRoles()

    watch(page, fetchRoles)

    return { roles, page, totalPages, fetchRoles, nextPage, prevPage }; 
}

