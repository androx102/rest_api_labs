import axios from 'axios'
import store from '../store'
import Cookies from 'js-cookie'

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1'
})

axiosInstance.interceptors.request.use(
  config => {
    const accessToken = Cookies.get('access_token')
    const refreshToken = Cookies.get('refresh_token')

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

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

axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const response = await axiosInstance.post('/token/refresh/')
        const { access } = response.data
        Cookies.set('access_token', access)
        originalRequest.headers.Authorization = `Bearer ${access}`
        
        return axiosInstance(originalRequest)
      } catch (refreshError) {
        
        store.dispatch('logout')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default axiosInstance