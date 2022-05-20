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
    if (err.response) {
      // Access Token was expired
      if (err.response.status === 401 && !originalConfig._retry) {
        originalConfig._retry = true
        try {
          
          const rs = await instance.post('/auth/token/refresh/', {
            refresh: localStorage.getItem('refreshToken'),
          }).catch(() => {
            console.log("expired")
            useAuthenticationStore().logout()
          })
          console.log("test")
          const { access } = (rs as any).data
          localStorage.setItem('accessToken', access)
          instance.defaults.headers.common.Authorization = `Bearer ${access}`
          return instance(originalConfig)
          
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (_error: any) {
          console.log("expired!")
          useAuthenticationStore().logout()
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
