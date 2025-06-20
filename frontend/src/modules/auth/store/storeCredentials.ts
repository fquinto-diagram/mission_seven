import { defineStore } from 'pinia';
import { useCookies } from 'vue3-cookies'
import type { Credentials } from '@/modules/auth/interface/credentials.interface';

const {cookies} = useCookies()

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
      cookies.remove('token')
      localStorage.removeItem('credentials');
      localStorage.removeItem('token');
    }
  }
});