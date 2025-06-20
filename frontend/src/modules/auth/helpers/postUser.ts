import api from "@/config/api";
import { useCookies } from 'vue3-cookies'
import type { Credentials } from "@/modules/auth/interface/credentials.interface";

const { cookies } = useCookies()


//Funcion asincrona que retorna data, dentro de ella estará el token

export async function postUser(credentials: Credentials ) {
    try {
        const response = await api.post<Credentials>('/login', credentials,)
        const { token } = response.data
        if(token){
            cookies.set('token', token)
        }
    } catch (error) {
        alert(`Hay un error: ${error}`)
    }
}
 