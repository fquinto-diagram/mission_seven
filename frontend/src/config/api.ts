import axios from "axios";
import { useCookies } from "vue3-cookies";

const api = axios.create({ 
    baseURL: import.meta.env.VITE_API_URL
});
const { cookies } = useCookies();

api.interceptors.request.use((config) => {
  const token = cookies.get('token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});
export default api;