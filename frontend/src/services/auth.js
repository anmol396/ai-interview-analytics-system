import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/auth';

export const authService = {
  signup: async (username, email, password) => {
    const response = await axios.post(`${API_URL}/signup`, {
      username,
      email,
      password
    });
    return response.data;
  },

  login: async (username, password) => {
    // Note: Fast API OAuth2PasswordRequestForm expects 'username' but we allow email too
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await axios.post(`${API_URL}/login`, formData);
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('isAuthenticated', 'true');
    }
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('isAuthenticated');
  },
  
  isAuthenticated: () => {
    return localStorage.getItem('isAuthenticated') === 'true';
  },
  
  getToken: () => localStorage.getItem('token')
};
