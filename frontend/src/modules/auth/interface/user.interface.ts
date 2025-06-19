export interface User{
    id: number
    name: string
    surname: string
    email: string
    password: string
    lang: string
    created_at?: Date
    deleted_at?: Date
}