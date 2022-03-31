import {defineStore} from 'pinia'
import {instance} from '../utils/axios'
import {convertObjectKeysToCamelCase} from '../utils/case-conversion'

export const useSkillStore = defineStore('skills', {
    state: () => ({
        skills: [],
        isLoadingSkills: false,
    }),
    actions: {
        /*
         * SKILLS
         */
        async loadSkills() {
            // start the loading animation
            this.isLoadingSkills = true
            this.skills = []
            instance
                .get('skills/')
                .then(({data}) => {
                    // turn of the loading animation
                    this.isLoadingSkills = false
                    // set the store
                    let apiSkills = convertObjectKeysToCamelCase(data).results
                    for (let skill of apiSkills) {
                        this.skills.push({
                            name: skill.name,
                            amount: 0,
                            comment: '',
                            url: skill.url,
                            id: skill.id,
                        })
                    }
                })
                .catch(() => (this.isLoadingSkills = false))
        },
        async addSkill(newSkill, callback) {
            // start the loading animation
            this.isLoadingSkills = true

            // Process the new skill
            console.log(`Adding new skill: ${newSkill}.`)
            this.skills.push({name: newSkill, amount: 0, comment: ''})

            // TODO: maybe only push skills to database when project POST happens
            // TODO: remove description (waiting for backend update)
            // TODO: add a ?color picker?
            instance
                .post('skills/', {
                    name: newSkill,
                    description: 'string',
                    color: 'string',
                })
                //TODO: response based feedback
                .then(function (response) {
                    console.log(response)
                })
                .catch(function (error) {
                    console.log(error)
                })

            // turn of the loading animation
            this.isLoadingSkills = false
            // When finished run the callback so the popup closes.
            callback(newSkill)
        },
        async deleteSkill(deletedSkill) {
            await instance
                .delete(`skills/${deletedSkill.id}/`)
                .then(() => {
                    const index = this.skills.findIndex(skill => skill.id === deletedSkill.id)
                    this.skills.splice(index, 1)
                })
                .catch(() => console.log("Failed to delete"))
        },

        /*
         * PROJECT TODO: move to a project store once that exists
         */
        submitProject(projectName, projectURL, partnerName, coaches, callback) {
            let data = {
                name: projectName,
                partner_name: partnerName,
                extra_info: projectURL,
                required_skills: [],
                coaches: [],
            }

            // filter out the used skills
            for (let skill of this.skills) {
                if (skill.amount > 0) {
                    data['required_skills'].push({
                        skill: skill.url,
                        amount: skill.amount,
                        // TODO: a project skill had no comment field yet (in database)
                        // comment: skill.comment,
                    })
                }
            }

            // add the selected coaches to data object
            coaches.forEach(coach => data.coaches.push(coach.url))

            // POST request to make a project
            instance
                .post('projects/', data)
                //TODO: response based feedback
                .then(function (response) {
                    console.log(response)
                })
                .catch(function (error) {
                    console.log(error)
                })

            callback()
        },
    },
})
