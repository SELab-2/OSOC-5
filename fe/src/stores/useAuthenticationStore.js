import axios from 'axios'
import { defineStore } from 'pinia'
import { setCsrfToken } from '../utils/axios'
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";
import router from "../router/index"

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
        setCsrfToken()

        this.loggedInUser = convertObjectKeysToCamelCase(data).user // doesn't work yet!

        router.push('/students')
      })
    },
    logout() {
      this.$reset()
    },
  },
})
