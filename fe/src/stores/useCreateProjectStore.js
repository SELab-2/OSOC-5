import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'


export const useCreateProjectStore = defineStore('skills', {
    state: () => ({
        skills: [],
        isLoadingSkills: false,
    }),
    actions: {
        async loadSkills() {
            // start the loading animation
            this.isLoadingSkills = true
            instance
                .get('skills/')
                .then(({ data }) => {
                    // turn of the loading animation
                    this.isLoadingSkills = false

                    let apiSkills = convertObjectKeysToCamelCase(data).results
                    for (let skill of apiSkills) {
                        this.skills.push({ name: skill.name, amount: 0, comment: '', url: skill.url })
                    }

                })
                .catch(() => (this.isLoadingSkills = false))
        },
        async addSkill(newSkill, callback) {
            // start the loading animation
            this.isLoadingSkills = true

            // Process the new skill
            console.log(`Adding new skill: ${newSkill}.`)
            this.skills.push({ name: newSkill, amount: 0, comment: '' })

            // TODO: verlopig maken we onmiddelijk een skill entry aan in de database
            //       maar dit kan eigelijk ook wanneer het project wordt aangemaakt
            //       zodanig dat je als je op cancel drukt de roles ook niet opslaat

            //TODO remove description and add a ?color picker?
            instance
                .post('skills/', { 'name': newSkill, 'description': 'string', 'color': 'string' })
                .then(function(response) {
                    console.log(response)
                    //TODO: als gelukt -> display added
                })
                .catch(function(error) {
                    console.log(error)
                    //TODO: als error -> display error
                })

            // turn of the loading animation
            this.isLoadingSkills = false
            // When finished run the callback so the popup closes.
            callback(newSkill)
        },
        clearSkills() {
            this.$reset()
        },
        submitProject(projectName, projectURL, partnerName, callback) {

            let data = {
                'name': projectName,
                'partner_name': partnerName,
                'extra_info': projectURL,
                'required_skills': [],
                'coaches': [],
            }

            // filter out the used skills
            for (let skill of this.skills) {
                if (skill.amount > 0) {
                    data['required_skills'].push({ 'skill': skill.url, 'amount': skill.amount })
                }
            }

            // TODO: skills kloppen nog niet helemaal er kan nog geen comment bij
            console.log(data)

            // POST request to make a rpoject
            instance
                .post('projects/', data)
                .then(function(response) {
                    console.log(response)
                    //TODO: als gelukt -> display added
                })
                .catch(function(error) {
                    console.log(error)
                    //TODO: als error -> display error
                })

            callback()
        },
    },
})
