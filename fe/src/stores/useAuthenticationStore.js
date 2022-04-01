import axios from 'axios'
import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";
// 
// interface State {
//   loggedInUser: { email: string; password: string } | undefined
// }

const host = 'http://localhost:8000/api/'

export const useAuthenticationStore = defineStore('user/authentication', {
  state: () => ({
    loggedInUser: undefined,
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

      this.loggedInUser = { email: email, password: password }
    },
    logout() {
      this.$reset()
    },
  },
})