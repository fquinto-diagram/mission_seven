import api from "@/config/api";

export async function deleteRol(id: number | undefined) {
    try {
        const response = await api.delete(`/roles/${id}`)
        return response.data
    } catch (error) {
        alert(`Hay algun error \n ${error}`)
    }
}