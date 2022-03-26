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

            // TODO: verlopig maken we onmiddelijk een skill entry aan in de database
            //       maar dit kan eigelijk ook wanneer het project wordt aangemaakt
            //       zodanig dat je als je op cancel drukt de roles ook niet opslaat

            //TODO remove description and add a ?color picker?
            instance
                .post('skills/', {})
                .then(function (response) {
                    console.log(response);
                    //TODO: als gelukt -> display added
                })
                .catch(function (error) {
                    console.log(error);
                    //TODO: als error -> display error
                });

            // When finished run the callback so the popup closes.
            callback(newSkill);
        },
        clearSkills() {
            this.$reset()
        },
    },
})
