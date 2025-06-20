export interface GetUserResponse{
    user: User
}

export interface User{
    name: string
    surname: string
    email: string
    lang: string
}