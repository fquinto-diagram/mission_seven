export interface LoginCredentials{
    email: string
    password: string
}
export interface ResponseToken{
    token: string
    user:{
        id: number,
        email: string
    }
}