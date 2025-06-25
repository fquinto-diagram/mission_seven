import api from "@/config/api";
import type { RolesResponse } from "@/modules/Roles/interfaces/role.interface";

export async function getRoles() {
    try {
        const response = await api.get<RolesResponse>('/roles');
        return response.data
    } catch (error) {
        alert(`Hay un error ${error}`)
    }
}