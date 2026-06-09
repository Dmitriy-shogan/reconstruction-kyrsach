import axios from 'axios';

const api = axios.create({
  baseURL: "https://backend-production-6392b.up.railway.app",
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  // Для загрузки файлов не устанавливаем Content-Type вручную
  // axios сам установит multipart/form-data с boundary
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }
  
  return config;
});

export default api;