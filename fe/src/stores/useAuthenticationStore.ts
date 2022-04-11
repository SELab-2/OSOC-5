import axios from 'axios'
import { defineStore } from 'pinia'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { User, UserInterface } from '../models/User'

const baseURL =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/api/'
    : 'https://sel2-5.ugent.be/api/'

interface State {
  loggedInUser: UserInterface | null
}

export const useAuthenticationStore = defineStore('user/authentication', {
  state: (): State => ({
    loggedInUser: null,
  }),
  actions: {
    async login({
      email,
      password,
    }: {
      email: string
      password: string
    }): Promise<void> {
      const { data } = await axios.post(baseURL + 'auth/login/', {
        username: email,
        email,
        password,
      })
      localStorage.setItem('refreshToken', data.refresh_token)
      localStorage.setItem('accessToken', data.access_token)

      this.loggedInUser = convertObjectKeysToCamelCase(data).user as User

      localStorage.setItem('refreshToken', data.refresh_token)
      localStorage.setItem('accessToken', data.access_token)
    },
    logout(): void {
      this.$reset()
    },
  },
})
