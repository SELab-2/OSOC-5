import { defineStore } from 'pinia'

// interface State {
//   users: Array<User>
//   isLoadingUsers: boolean
// }

export const useCoachStore = defineStore('user/coach', {
  state: () => ({
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
      return instance
        .put(`coaches/${user.id}/${newRole === "admin" ? 'make' : 'remove'}_admin/`)
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
