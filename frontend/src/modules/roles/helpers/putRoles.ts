import type { Rol } from "@/modules/roles/interfaces/role.interface";
import api from "@/config/api";

export async function putRol(id: number|undefined, payload: Rol) {
  try {
    const response = await api.put(`/roles/${id}`, payload);
    return response.data;
  } catch (error) {
    alert(`Error al actualizar el rol ${id}: ${error}`);
    throw error;
  }
}