import { defineStore } from 'pinia'
import { User, UserInterface } from '../models/User'
import { instance } from '../utils/axios'
import { useAuthenticationStore } from './useAuthenticationStore'

interface State {
  users: Array<User>
  isLoading: boolean
}

export const useCoachStore = defineStore('user/coach', {
  state: (): State => ({
    users: [],
    isLoading: false,
  }),
  actions: {
    /**
     * If we already have the user return it, otherwise fetch it
     * @param newUser user to be fetched
     * @returns the requested user
     */
    async getUser(newUser: UserInterface): Promise<User> {
      const user = this.users.find((user) => (user && newUser) ? user.url === newUser.url : false)

      if (user) return user
      let fetchedUser: User
      if (useAuthenticationStore().loggedInUser?.isAdmin && newUser) {
        // Logged in user is admin and can fetch users.
        const { data } = await instance.get<UserInterface>(newUser.url)
        fetchedUser = new User(data)
      } else {
        // Logged in user is coach and cannot fetch users.
        fetchedUser = new User(newUser)
      }

      // Check again if not present, it could be added in the meantime.
      const user2 = this.users.find((user) => (user && newUser) ? user.url === newUser.url : false)
      if (user2) return user2

      if (fetchedUser) this.users.push(fetchedUser)
      return fetchedUser
    },
    /**
     * Loads the users
     */
    async loadUsers() {
      this.isLoading = true
      const { results } = (
        await instance.get<{ results: UserInterface[] }>(
          'coaches/?page_size=500'
        )
      ).data
      this.users = results.map((user) => new User(user))
      this.isLoading = false
    },
    
    async loadNext(index: number, done: Function, filters: Object): Promise<Array<User>> {
      
      const { results, next } = (await instance.get<{ results: User[], next: string }>(`coaches/?page=${index}`, { params: filters })).data
      
      done(next === null)
      return results.map(u => new User(u))
    },
    
    async loadUsersCoaches(filters: Object, setNumberOfRows: Function) {
      this.isLoading = true

      const { results, count } = (
        await instance.get<{ results: UserInterface[]; count: number }>(
          "coaches/", {
            params: filters
            }
        )
      ).data

      setNumberOfRows(count)
      this.users = results.map((user) => new User(user))

      this.isLoading = false
    },
    /**
     * Updates the role from a user
     * @param user the user from which we want to change the role
     * @returns the updated user
     */
    async updateRole(user: User) {
      return instance.put(`coaches/${user.id}/update_status/`, {
        is_admin: user.isAdmin,
        is_active: user.isActive,
      })
    },
    /**
     * Removes a user from the database
     * @param userId id of the user which we want to remove
     */
    async removeUser(userId: number, success: Function, fail: Function) {
      await instance
        .delete(`coaches/${userId}/`)
        .then(() => success())
        .catch(() => fail())
    },
    clearUsers() {
      this.$reset()
    },
  },
})
