import axios from 'axios'
import { defineStore } from 'pinia'
import { StoreDefinition } from 'pinia'
import router from "../router/index"

const baseURL =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/api/'
    : 'https://sel2-5.ugent.be/api/'

export const useAuthenticationStore: StoreDefinition<
  'user/authentication',
  {
    loggedInUser: { first_name: string, last_name: string, email: string; password: string } | Record<string, unknown>
  },
  Record<string, never>,
  {
    login({
      email,
      password,
    }: {
      first_name: string
      last_name: string
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
      const {data} = await axios.post('http://localhost:8000/api/auth/login/', {
        username: email,
        email,
        password,
      })

      localStorage.setItem("refreshToken", data.refresh_token)
      localStorage.setItem("accessToken", data.access_token)

      this.loggedInUser = { first_name: data.user.first_name, last_name: data.user.last_name, email: email, password: password }

      router.push('/users')
    },
    async logout() {
      localStorage.removeItem("refreshToken")
      localStorage.removeItem("accessToken")
      router.push('/')
      // this.$reset()
    },
  },
})