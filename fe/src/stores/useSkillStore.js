import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'


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

                    let apiSkills = convertObjectKeysToCamelCase(data).results
                    for(let skill of apiSkills){
                        this.skills.push({name: skill.name, amount:0, comment:""})
                    }

                })
                .catch(() => (this.isLoadingSkills = false))
        },
        async addSkill(newSkill, callback) {
            // Process the new skill
            console.log(`Adding new skill: ${newSkill}.`)
            this.skills.push({ name: newSkill, amount: 0, comment: '' })

            // When finished run the callback so the popup closes.
            callback(newSkill);
        },
        clearSkills() {
            this.$reset()
        },
    },
})
