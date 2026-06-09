import axios from 'axios';

// ЖЁСТКО ПРОПИСАНО HTTPS - НИКАКИХ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
const API_URL = 'https://backend-production-6392b.up.railway.app';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  // Для FormData не устанавливаем Content-Type вручную
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }
  
  return config;
});

export default api;