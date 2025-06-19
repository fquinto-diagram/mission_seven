import api from "@/config/api";
import { useCookies } from 'vue3-cookies'
import type { User } from "@/modules/auth/interface/user.interface";

// Funcion para coger el nombre del usuario de dentro de la base de datos.

export async function getUser() {
    try {
        const { cookies }= useCookies()
        const token = cookies.get('token')
        const response = await api.get<User>('/profile', {
            headers:{
                Authorization: `Bearer ${token}`
            }
        })
        return response
    } catch (error) {
        alert(`Hay un error: ${error}`)
    }
}
 