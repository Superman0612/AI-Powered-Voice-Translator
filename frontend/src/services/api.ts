import axios from 'axios';
import type {
  Language,
  User,
  TranslationRecord,
  LanguageDetectResponse,
  ModelRegistryItem,
  EvaluationSummary
} from '../types';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('bhashaai_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Response interceptor to handle session expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const isLoginOrRegister = error.config?.url?.includes('/auth/login') || error.config?.url?.includes('/auth/register');
    const isUserNotFound = error.response?.status === 404 && String(error.response?.data?.detail || '').toLowerCase().includes('user');
    
    if ((error.response?.status === 401 || isUserNotFound) && !isLoginOrRegister) {
      localStorage.removeItem('bhashaai_token');
      localStorage.removeItem('bhashaai_user');
    }
    return Promise.reject(error);
  }
);

export const api = {
  // Authentication
  auth: {
    login: async (email: string, password: string) => {
      const response = await apiClient.post('/auth/login/json', { email, password });
      return response.data; // { access_token, token_type, expires_in }
    },
    register: async (data: { email: string; username: string; password: string; full_name?: string }) => {
      const response = await apiClient.post('/auth/register', data);
      return response.data as User;
    },
    getMe: async () => {
      const response = await apiClient.get('/auth/me');
      return response.data as User;
    },
    logout: async () => {
      try {
        await apiClient.post('/auth/logout');
      } catch (e) {
        // Continue client-side cleanup even if server is unreachable
      }
      localStorage.removeItem('bhashaai_token');
      localStorage.removeItem('bhashaai_user');
    }
  },

  // Languages Catalog
  languages: {
    list: async () => {
      const response = await apiClient.get('/languages');
      return response.data as Language[];
    },
    get: async (code: string) => {
      const response = await apiClient.get(`/languages/${code}`);
      return response.data as Language;
    },
    detect: async (text: string) => {
      const response = await apiClient.post('/languages/detect', { text });
      return response.data as LanguageDetectResponse;
    }
  },

  // Translation Services
  translate: {
    text: async (data: { source_text: string; target_language: string; source_language?: string }) => {
      const response = await apiClient.post('/translate/text', data);
      return response.data as TranslationRecord;
    },
    voice: async (formData: FormData, onUploadProgress?: (progressEvent: any) => void) => {
      const response = await apiClient.post('/translate/voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress,
      });
      return response.data as TranslationRecord;
    },
    getHistory: async (skip = 0, limit = 20) => {
      const response = await apiClient.get('/translate/history', {
        params: { skip, limit }
      });
      return response.data as TranslationRecord[];
    },
    getById: async (id: string) => {
      const response = await apiClient.get(`/translate/${id}`);
      return response.data as TranslationRecord;
    },
    delete: async (id: string) => {
      const response = await apiClient.delete(`/translate/${id}`);
      return response.data;
    }
  },

  // Audio Vault
  audio: {
    upload: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      const response = await apiClient.post('/audio/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    },
    getDownloadUrl: (audioId: string) => {
      return `${API_BASE_URL}/audio/${audioId}/download`;
    }
  },

  // ML Evaluation & Benchmarks
  evaluation: {
    getModels: async () => {
      const response = await apiClient.get('/evaluation/models');
      return response.data as ModelRegistryItem[];
    },
    getSummary: async () => {
      const response = await apiClient.get('/evaluation/summary');
      return response.data as EvaluationSummary;
    }
  },

  // Diagnostics & Health
  health: {
    check: async () => {
      const response = await apiClient.get('/health');
      return response.data;
    }
  }
};

export default api;

