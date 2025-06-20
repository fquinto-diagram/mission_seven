import api from "@/config/api";
import type { User } from "@/modules/auth/interface/user.interface";

// Funcion para coger el nombre del usuario de dentro de la base de datos.

export async function getUser(token: string) {
    try {
        const response = await api.get<User>('/profile', {
            headers:{
                Authorization: `Bearer ${token}`
            }
        })
        return response.data
    } catch (error) {
        alert(`Hay un error: ${error}`)
    }
}
 