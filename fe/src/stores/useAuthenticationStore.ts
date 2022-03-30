import axios from 'axios'
import { defineStore } from 'pinia'
import { setCsrfToken } from '../utils/axios'
import { StoreDefinition } from 'pinia'

const baseURL =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/'
    : 'https://sel2-5.ugent.be/'

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
      await axios.post(
        baseURL + 'api/login/',
        {
          username: email,
          email,
          password,
        },
        { withCredentials: true }
      )

      setCsrfToken()

      this.loggedInUser = { email, password }
    },
    logout() {
      this.$reset()
    },
  },
})
