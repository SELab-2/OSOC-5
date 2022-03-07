import { defineStore } from 'pinia'

interface State {
    firstName: string
    lastName: string
    userId: number | null
}

export const useAuthUserStore = defineStore('auth/user', {
    state: (): State => ({
        firstName: '',
        lastName: '',
        userId: null,
    }),
    getters: {
        fullName: (state) => `${state.firstName} ${state.lastName}`,
        loggedIn: (state) => state.userId !== null,
    },
    actions: {
        async loadUser(id: number) {
            if (this.userId !== null) throw new Error('Already logged in')

            this.updateUser({ firstName: 'Test', lastName: 'test', userId: 0 })
        },
        updateUser(payload: {
            firstname?: string
            lastName: any
            userId: any
            firstName?: any
        }) {
            this.firstName = payload.firstName
            this.lastName = payload.lastName
            this.userId = payload.userId
        },
        // easily reset state using `$reset`
        clearUser() {
            this.$reset()
        },
    },
})
