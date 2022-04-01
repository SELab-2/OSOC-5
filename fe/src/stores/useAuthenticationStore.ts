import axios from 'axios'
import { defineStore } from 'pinia'
import { StoreDefinition } from 'pinia'

const baseURL =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/api/'
    : 'https://sel2-5.ugent.be/api/'

export const useAuthenticationStore: StoreDefinition<
  'user/authentication',
  {
    loggedInUser: { email: string; password: string } | Record<string, unknown>
  },
  Record<string, never>,
  {
    login({
      email,
      password,
    }: {
      email: string
      password: string
    }): Promise<void>
    logout(): void
  }
> = defineStore('user/authentication', {
  state: () => ({
    loggedInUser: {},
  }),
  actions: {
    async login({ email, password }) {
      const { data } = await axios.post(baseURL + 'auth/login/', {
        username: email,
        email,
        password,
      })

      localStorage.setItem('refreshToken', data.refresh_token)
      localStorage.setItem('accessToken', data.access_token)

      this.loggedInUser = { email, password }
    },
    logout() {
      this.$reset()
    },
  },
})
