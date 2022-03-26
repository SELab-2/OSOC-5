import axios from 'axios'
import { defineStore } from 'pinia'
import { setCsrfToken } from '../utils/axios'
// 
// interface State {
//   loggedInUser: { email: string; password: string } | undefined
// }

const host = 'http://localhost:3000'

export const useAuthenticationStore = defineStore('user/authentication', {
  state: () => ({
    loggedInUser: undefined,
  }),
  actions: {
    // https://sel2-5.ugent.be
    // admin@example.com
    async login({ email, password }) {
      await axios.post('http://localhost:8000/api/login/', {
        username: email,
        email,
        password,
      },{withCredentials: true}).then(function() {
        window.location.href = host + '/students'
      })

      setCsrfToken()

      this.loggedInUser = { email, password }
    },
    logout() {
      this.$reset()
    },
  },
})
