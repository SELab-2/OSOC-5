import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'

// interface State {
//   skills: Array<User>
//   isLoadingSkills: boolean
// }

export const useSkillStore = defineStore('skills', {
    state: () => ({
        skills: [],
        isLoadingSkills: false,
    }),
    actions: {
        async loadSkills() {
            this.isLoadingSkills = true
            instance
                .get('skills/')
                .then(({ data }) => {
                    this.isLoadingSkills = false
                    // this.skills = convertObjectKeysToCamelCase(data).results
                    let apiSkills = convertObjectKeysToCamelCase(data).results
                    for(let skill of apiSkills){
                        this.skills.push({name: skill.name, amount:0, comment:""})
                    }
                    // this.skills.forEach(user => {user.role = user.isAdmin ? 'admin' : 'coach'})
                })
                .catch(() => (this.isLoadingSkills = false))
        },
        async updateRole(user, newRole, callback) {
            console.log(`Will update role to ${newRole} for ${user.firstName} ${user.lastName}`)
            callback();
        },
        // async removeUser(userId) {
        //     await instance
        //         .delete(`coaches/${userId}/`)
        //         .then(() => {
        //             const index = this.skills.findIndex(user => user.id === userId)
        //             this.skills.splice(index,1)
        //         })
        //         .catch(() => console.log("Failed to delete"))
        // },
        // clearSkills() {
        //     this.$reset()
        // },
    },
})
