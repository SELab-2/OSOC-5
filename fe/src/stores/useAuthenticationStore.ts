import axios from 'axios'
import { defineStore } from 'pinia'
import { setCsrfToken } from '../utils/axios'

interface State {
  loggedInUser: { email: string; password: string } | undefined
}

export const useAuthenticationStore = defineStore('user/authentication', {
  state: (): State => ({
    loggedInUser: undefined,
  }),
  actions: {
    // https://sel2-5.ugent.be
    // admin@example.com
    async login({ email, password }: { email: string; password: string }) {
      await axios.post('http://localhost:8000/api/login/', {
        username: email,
        email,
        password,
      },{withCredentials: true})

      setCsrfToken()

      this.loggedInUser = { email, password }
    },
    logout() {
      this.$reset()
    },
  },
})
