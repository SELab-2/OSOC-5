import axios, { AxiosInstance } from 'axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { baseUrl } from './baseUrl'
import router from "../router";

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
    return convertObjectKeysToCamelCase(res as any)
  },
  async (err) => {
    const originalConfig = err.config
    if (err.response) {
      // Access Token was expired
      if (err.response.status === 401 && !originalConfig._retry) {
        originalConfig._retry = true
        try {
          const rs = await refreshToken(instance)
          const { access } = rs.data
          localStorage.setItem('accessToken', access)
          instance.defaults.headers.common.Authorization = `Bearer ${access}`
          return instance(originalConfig)
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

function refreshToken(instance: AxiosInstance) {
  return instance.post('/auth/token/refresh/', {
    refresh: localStorage.getItem('refreshToken'),
  }).catch(() => router.push('/login'))
}
