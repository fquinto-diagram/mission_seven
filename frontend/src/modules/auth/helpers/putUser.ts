import api from "@/config/api";
import type { User } from "@/modules/auth/interface/user.interface";

export async function putUser(token: string, newUser: User) {
    try {
        const response = await api.put('/profile', newUser,{
            headers:{
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
            }});
        return response.data
    } catch (error) {
        alert(`Hay un error ${error}`)
    }
}