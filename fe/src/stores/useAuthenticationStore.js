import axios from 'axios'
import { defineStore } from 'pinia'
import { setCsrfToken } from '../utils/axios'
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";
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
      },{withCredentials: true}).then(({data}) => {
        console.log({ email: email, password: password })
        setCsrfToken()

        // this.loggedInUser = convertObjectKeysToCamelCase(data).results // doesn't work yet!

        this.loggedInUser = { email: email, password: password }

        window.location.href = host + '/students'
      })
    },
    logout() {
      this.$reset()
    },
  },
})
