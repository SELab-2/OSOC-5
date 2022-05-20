import axios, { AxiosInstance } from 'axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { baseUrl } from './baseUrl'
import { useAuthenticationStore } from '../stores/useAuthenticationStore'

export const instance: AxiosInstance = axios.create({
  baseURL: baseUrl,
})

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers && (config.headers.Authorization = `Bearer ${token}`)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

instance.interceptors.response.use(
  (res) => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return convertObjectKeysToCamelCase(res as any)
  },
  async (err) => {
    const originalConfig = err.config
    if (originalConfig.url === '/auth/token/refresh/') {
      // Logout if the token couldn't be refreshed.
      useAuthenticationStore().logout()
    }
    if (err.response) {
      // Access Token was expired
      if (err.response.status === 401 && !originalConfig._retry) {
        originalConfig._retry = true
        try {
          console.log("test")
          const rs = await instance.post('/auth/token/refresh/', {
            refresh: localStorage.getItem('refreshToken'),
          })
          
          const { access } = rs.data
          localStorage.setItem('accessToken', access)
          instance.defaults.headers.common.Authorization = `Bearer ${access}`
          return instance(originalConfig)
          
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (_error: any) {
          if (_error.response && _error.response.data) {
            return Promise.reject(_error.response.data)
          }
          return Promise.reject(_error)
        }
      }
      if (err.response.status === 403 && err.response.data) {
        return Promise.reject(err.response.data)
      }
    }
    return Promise.reject(err)
  }
)
