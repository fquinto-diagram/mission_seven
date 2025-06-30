import api from "@/config/api";
import type { RolesResponse } from "@/modules/roles/interfaces/role.interface";

export async function getAllRoles(page = 1) {
    try {
        const response = await api.get<RolesResponse>(`/roles?limit=4&page=${page}`);
        return response.data
    } catch (error) {
        alert(`Hay un error ${error}`)
    }
}
