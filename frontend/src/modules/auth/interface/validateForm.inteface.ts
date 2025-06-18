export interface LoginCredentials{
    email: string
    password: string
}
export interface userStore{
    token: string
    user:{
        id: number,
        email: string
    }
}