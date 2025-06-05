import axios from 'axios'
import store from '../store'
import Cookies from 'js-cookie'

// Create axios instance with base URL
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1'
})

// Request interceptor
axiosInstance.interceptors.request.use(
  config => {
    const accessToken = Cookies.get('access_token')
    const refreshToken = Cookies.get('refresh_token')

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    // If it's a refresh token request, include refresh token in body
    if (config.url === '/token/refresh/') {
      config.data = {
        ...config.data,
        refresh: refreshToken
      }
    }

    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // If error is 401 and we haven't tried to refresh token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh the token
        const response = await axiosInstance.post('/token/refresh/')
        const { access } = response.data

        // Store new access token
        Cookies.set('access_token', access)
        
        // Retry the original request
        originalRequest.headers.Authorization = `Bearer ${access}`
        return axiosInstance(originalRequest)
      } catch (refreshError) {
        // If refresh fails, logout user
        store.dispatch('logout')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default axiosInstance