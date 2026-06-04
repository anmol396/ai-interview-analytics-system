import axios from 'axios';

// Use VITE env var if available, otherwise fall back to hardcoded local address
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

console.log(`[API] Configured base URL: ${BASE_URL}`);

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ── Request interceptor: attach JWT token to every request ────────────────────
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log(`[API] ➡ ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] Request setup error:', error);
    return Promise.reject(error);
  }
);

// ── Response interceptor: log results and handle auth errors ──────────────────
api.interceptors.response.use(
  (response) => {
    console.log(
      `[API] ✅ ${response.status} ${response.config.url}`,
      response.data
    );
    return response;
  },
  (error) => {
    const status = error.response?.status;
    const url    = error.config?.url;

    console.error(`[API] ❌ ${status ?? 'NETWORK'} ${url}:`, error.message);

    // Auto-logout on expired / invalid token
    if (status === 401) {
      console.warn('[API] 401 Unauthorized — clearing session and redirecting to login');
      localStorage.removeItem('token');
      localStorage.removeItem('isAuthenticated');
      window.location.href = '/';
    }

    return Promise.reject(error);
  }
);

// ── API surface ───────────────────────────────────────────────────────────────
export const candidateAPI = {
  getAll:   ()           => api.get('/candidates'),
  getById:  (id)         => api.get(`/candidates/${id}`),
  create:   (data)       => api.post('/add-candidate', data),
  update:   (id, data)   => api.put(`/candidates/${id}`, data),
  delete:   (id)         => api.delete(`/candidates/${id}`),
};

export const analyticsAPI = {
  getStats:  () => api.get('/dashboard-stats'),
  getHealth: () => api.get('/health'),
};

export const aiAPI = {
  chat: (data) => api.post('/chat', data),
  getFullList: (filterKey) => api.get(`/chat/full-list?filter_key=${encodeURIComponent(filterKey)}`),
};

export const healthCheck = () => api.get('/health');

export default api;
