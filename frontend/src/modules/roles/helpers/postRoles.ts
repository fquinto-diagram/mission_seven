import api from "@/config/api";
import type { Rol } from "@/modules/roles/interfaces/role.interface";

export async function postRoles(newRol: Rol) {
    try {
        const response = await api.post<Rol>(`/roles`, newRol)
        return response.data
    } catch (error) {
        alert(`Hay algun error\n ${error}`)
    }
}