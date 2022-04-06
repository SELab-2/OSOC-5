import { defineStore } from 'pinia'
import { User, UserInterface } from '../models/User'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'

interface State {
  users: Array<UserInterface>
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
          this.users = convertObjectKeysToCamelCase(data) as any as User[]
          this.users.forEach((user) => {
            user.role = user.isAdmin ? 'admin' : 'coach'
          })
        })
        .catch(() => (this.isLoadingUsers = false))
    },
    async updateRole(user: { id: Number }, newRole: string) {
      return instance.put(
        `coaches/${user.id}/${newRole === 'admin' ? 'make' : 'remove'}_admin/`
      )
    },
    async removeUser(userId: number) {
      await instance
        .delete(`coaches/${userId}/`)
        .then(() => {
          const index = this.users.findIndex((user) => user.id === userId)
          this.users.splice(index, 1)
        })
        .catch(() => console.log('Failed to delete'))
    },
    clearUsers() {
      this.$reset()
    },
  },
})
