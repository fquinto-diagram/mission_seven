import api from "@/config/api";
import type { User } from "@/modules/auth/interface/user.interface";

export async function putUser(newUser: User) {
    try {
        const response = await api.put('/profile', newUser);
        return response.data
    } catch (error) {
        alert(`Hay un error ${error}`)
    }
}