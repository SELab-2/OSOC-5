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
          this.users = convertObjectKeysToCamelCase(data).results
          this.users.forEach(user => {user.role = user.isAdmin ? 'admin' : 'coach'})
        })
        .catch(() => (this.isLoadingUsers = false))
    },
    async updateRole(user, newRole, callback) {
      console.log(`Will update role to ${newRole} for ${user.firstName} ${user.lastName}`)
      callback();
    },
    async removeUser(userId) {
      await instance
      .delete(`coaches/${userId}/`)
      .then(() => {
        const index = this.users.findIndex(user => user.id === userId)
        this.users.splice(index,1)
      })
      .catch(() => console.log("Failed to delete"))
    },
    clearUsers() {
      this.$reset()
    },
  },
})
