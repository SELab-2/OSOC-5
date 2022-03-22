import axios from 'axios'
import { defineStore } from 'pinia'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'

interface State {
  loggedInUser: User | undefined
  token: String
}

export const useAuthenticationStore = defineStore('user/authentication', {
  state: (): State => ({
    loggedInUser: undefined,
    token: '',
  }),
  actions: {
    // https://sel2-5.ugent.be
    async login(credentials: { email: String; password: String }) {
      axios
        .post('http://localhost:8000/api/login', credentials)
        .then(({ data }) => {
          console.log(data)
          //   this.isLoadingUsers = false
          //   this.users = data.map((u: Object) => convertObjectKeysToCamelCase(u))
        })
      // .catch(() => (this.isLoadingUsers = false))
    },
    logout() {
      this.$reset()
    },
  },
})
