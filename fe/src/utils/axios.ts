import axios, { AxiosInstance } from 'axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'

export const instance: AxiosInstance = axios.create({
  baseURL:
    process.env.NODE_ENV == 'development'
      ? 'http://127.0.0.1:8000/api/'
      : 'https://sel2-5.ugent.be/api/',
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
  })
}
