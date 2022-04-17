import axios from 'axios'
import { defineStore } from 'pinia'
import { StoreDefinition } from 'pinia'
import router from "../router/index"
import { instance } from '../utils/axios'

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
    changePassword({
      p1,
      p2,
    }: {
      p1: string
      p2: string
    }): Promise<void>
  }
> = defineStore('user/authentication', {
  state: () => ({
    loggedInUser: {first_name:"NO LOGIN", last_name:"NO LOGIN",email:"NO LOGIN",password:"NO LOGIN"},
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
    async changePassword({p1, p2}) {
      const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` }
      };
      const bodyParameters = {
        new_password1: p1,
        new_password2: p2,
      };
      const {data} = await axios.post('http://localhost:8000/api/auth/password/change/', bodyParameters, config)
      this.loggedInUser = { first_name: this.loggedInUser.first_name, last_name: this.loggedInUser.last_name, email: this.loggedInUser.email, password: p1 }

    },
  },
})