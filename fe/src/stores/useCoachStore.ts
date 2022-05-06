import { defineStore } from 'pinia'
import { User, UserInterface } from '../models/User'
import { instance } from '../utils/axios'
import { useAuthenticationStore } from './useAuthenticationStore'

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
    async getUser(newUser: UserInterface): Promise<User> {
      const user = this.users.find((user) => user.url === newUser.url)
      if (user) return user
      let fetchedUser: User
      if (useAuthenticationStore().loggedInUser?.isAdmin) {
        // Logged in user is admin and can fetch users.
        const { data } = await instance.get<UserInterface>(newUser.url)
        fetchedUser = new User(data)
      } else {
        // Logged in user is coach and cannot fetch users.
        fetchedUser = new User(newUser)
      }

      // Check again if not present, it could be added in the meantime.
      const user2 = this.users.find((user) => user.url === newUser.url)
      if (user2) return user2

      this.users.push(fetchedUser)
      return fetchedUser
    },
    async loadUser(url: string) {
      const user = this.users.find((user) => user.url === url)
      if (user) return user

      const { data } = await instance.get<UserInterface>(url)
      return new User(data)
    },
    async loadUsers() {
      this.isLoadingUsers = true
      const { results } = (
        await instance.get<{ results: UserInterface[] }>('coaches')
      ).data
      this.users = results.map((user) => new User(user))
      this.isLoadingUsers = false
    },
    async updateRole(user: User) {
      return instance.put(`coaches/${user.id}/update_status/`, {
        is_admin: user.isAdmin,
        is_active: user.isActive,
      })
    },
    async removeUser(userId: number) {
      await instance
        .delete(`coaches/${userId}/`)
        .catch(() => console.log('Failed to delete'))

      const index = this.users.findIndex((user) => user.id === userId)
      this.users.splice(index, 1)
    },
    clearUsers() {
      this.$reset()
    },
  },
})
