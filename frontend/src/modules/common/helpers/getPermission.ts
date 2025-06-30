import api from "@/config/api";
import type { PermissionsResponse } from "@/modules/roles/interfaces/permission.interface";

export async function getAllPermissions() {
    try {
        const response = await api.get<PermissionsResponse>('/roles/permissions')
        return response.data
    } catch (error) {
        alert(`Hay algun error\n ${error}`)
    }
}