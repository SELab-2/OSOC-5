import axios from 'axios'
import { defineStore } from 'pinia'
import { StoreDefinition } from 'pinia'
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";
import router from "../router";
import {User} from "../models/User";

const baseURL =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/api/'
    : 'https://sel2-5.ugent.be/api/'

interface State {
  loggedInUser: User | null
}

export const useAuthenticationStore = defineStore('user/authentication', {
  state: (): State => ({
    loggedInUser: null,
  }),
  actions: {
    async login({ email, password }: {email: string, password: string}): Promise<void> {
      const { data } = await axios.post(baseURL + 'auth/login/', {
        username: email,
        email,
        password,
      })

      this.loggedInUser = convertObjectKeysToCamelCase(data).user as User

      localStorage.setItem("refreshToken", data.refresh_token)
      localStorage.setItem("accessToken", data.access_token)

      await router.push('/students')
    },
    logout(): void {
      this.$reset()
    },
  },
})
