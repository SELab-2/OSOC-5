import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'

interface State {
  users: Array<User>
  isLoadingUsers: boolean
}

export const useCoachStore = defineStore('user/coach', {
  state: (): State => ({
    users: [],
    isLoadingUsers: false,
  }),
  actions: {
    async loadUsers() {
      this.isLoadingUsers = true

      instance
        .get('coaches/')
        .then(({ data }) => {
          this.isLoadingUsers = false
          this.users = data.map((u: Object) => convertObjectKeysToCamelCase(u))
        })
        .catch(() => (this.isLoadingUsers = false))
    },
    clearUsers() {
      this.$reset()
    },
  },
})
