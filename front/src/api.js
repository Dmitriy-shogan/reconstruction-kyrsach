import axios from 'axios';

const api = axios.create({
  baseURL: '',  // ← ПУСТАЯ СТРОКА! Относительные пути
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