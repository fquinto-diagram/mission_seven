// src/stores/auth.ts
import { defineStore } from 'pinia';
import type { Credentials } from '@/modules/auth/interface/credentials.interface';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    credentials: JSON.parse(localStorage.getItem('credentials') || 'null') as Credentials | null,
    token: localStorage.getItem('token') || '',
  }),
  actions: {
    setCredentials(credentials: Credentials) {
      this.credentials = credentials;
      localStorage.setItem('credentials', JSON.stringify(credentials));
    },
    setToken(token: string) {
      this.token = token;
      localStorage.setItem('token', token);
    },
    logOut() {
      this.credentials = null;
      this.token = '';
      localStorage.removeItem('credentials');
      localStorage.removeItem('token');
    }
  }
});