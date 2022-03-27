import axios from 'axios'
import { defineStore } from 'pinia'
import { setCsrfToken } from '../utils/axios'
// 
// interface State {
//   loggedInUser: { email: string; password: string } | undefined
// }

const host = 'http://localhost:3000' //'https://sel2-5.ugent.be' 'http://localhost:3000'

export const useAuthenticationStore = defineStore('user/authentication', {
  state: () => ({
    loggedInUser: undefined,
  }),
  actions: {
    // https://sel2-5.ugent.be
    // admin@example.com
    async login({ email, password }) {
      //'https://sel2-5.ugent.be/api/login/' 'http://localhost:8000/api/login/'
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
