import type { LoginCredentials, userStore } from "../interface/validateForm.inteface";
import axios, { AxiosError } from "axios";
import api from "@/config/api";

export async function useLogin(credentials: LoginCredentials) {
    if (!credentials.email || !credentials.password) {
        throw new Error('Email and password are required');
    }

    try {
        const response = await api.post<userStore>('/login', credentials);
        
        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            return response.data;
        } else {
            throw new Error('Invalid response from server');
        }
    } catch (error) {
        if (axios.isAxiosError(error)) {
            const axiosError = error as AxiosError;
            if (!axiosError.response) {
                throw new Error('Network error - please check your connection');
            }
            if (axiosError.response.status === 401) {
                throw new Error('Invalid email or password');
            }
            throw new Error((axiosError.response?.data as { message?: string })?.message || 'Authentication failed');
        }
        throw error;
    }
}