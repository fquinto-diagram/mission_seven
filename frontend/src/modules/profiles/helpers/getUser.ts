import api from "@/config/api";
import type { User } from "@/modules/auth/interface/user.interface";

export async function getUser() {
    try {
        const response = await api.get<User>('/profile')
        return response.data
    } catch (error) {
        alert(`Hay un error: ${error}`)
    }
}
 