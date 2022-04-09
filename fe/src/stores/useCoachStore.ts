import { defineStore } from 'pinia'
import { User, UserInterface } from '../models/User'
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
    async getUser(url: string): Promise<User> {
      const user = this.users.find(user => user.url === url)
      if (user) return user;
      let { data } = await instance.get<UserInterface>(url)
      
      // Check again if not present, it could be added in the meantime.
      const user2 = this.users.find(user => user.url === url)
      if (user2) return user2
      
      let newUser = new User(data)
      this.users.push(newUser)
      return newUser
    },
    async loadUsers() {
      this.isLoadingUsers = true
      let { data } = await instance.get<UserInterface[]>('coaches')
      this.users = data.map(user => new User(user))
    },
    async updateRole(user: User) {
      return instance.put(
        `coaches/${user.id}/update_status/`,
        {
          is_admin: user.isAdmin,
          is_active: user.isActive
        }
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
