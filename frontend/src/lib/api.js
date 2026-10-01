const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
const TOKEN_KEY = 'ngombebora_access_token';

export function getAuthToken() {
  return window.sessionStorage.getItem(TOKEN_KEY);
}

export function setAuthToken(token) {
  window.sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearAuthToken() {
  window.sessionStorage.removeItem(TOKEN_KEY);
}

export async function api(path, options = {}) {
  const token = getAuthToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await response.json();
  if (response.status === 401 && !path.startsWith('/auth/login')) {
    clearAuthToken();
    window.dispatchEvent(new Event('ngombebora:session-expired'));
  }
  if (!response.ok) throw new Error(data.error || data.msg || 'Something went wrong');
  return data;
}
