import api from '@/config/api'
import type { Rol } from '../interfaces/role.interface';

export async function getRolById(id: number) {
  try {
        const response = await api.get<{role: Rol}>(`/roles/${id}?include[]=permissions`)
        return response.data
    } catch (error) {
        alert(`Error al obtener permisos del rol ${id}`);
        return [];
    }
}