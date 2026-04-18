import axios from 'axios'

const api = axios.create({
  baseURL: '/api/',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const role = sessionStorage.getItem('user_role')
  if (role) {
    config.headers['X-User-Role'] = role
  }
  return config
})

export default api
