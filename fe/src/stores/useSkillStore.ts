import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { ProjectSkill, Skill } from '../models/Skill'
import { Project } from '../models/Project'
import { User } from '../models/User'

interface State {
  skills: Array<ProjectSkill>
  isLoadingSkills: boolean
}

export const useSkillStore = defineStore('skills', {
  state: (): State => ({
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
        .then(({ data }) => {
          // turn of the loading animation
          this.isLoadingSkills = false
          // set the store
          const apiSkills = convertObjectKeysToCamelCase(data)
            .results as Skill[]
          for (const skill of apiSkills) {
            this.skills.push({
              name: skill.name,
              amount: 0,
              comment: '',
              url: skill.url,
              id: skill.id,
              description: '', // TODO REMOVE ON DATABASE UPDATE ISSUE #110
            })
          }
        })
        .catch(() => (this.isLoadingSkills = false))
    },
    async addSkill(newSkill: string) {
      // start the loading animation
      this.isLoadingSkills = true

      // Process the new skill
      console.log(`Adding new skill: ${newSkill}.`)
      // TODO: this new skill also needs to know it's url and id
      this.skills.push({
        name: newSkill,
        amount: 0,
        comment: '',
        url: '',
        id: -1,
        description: '',
      })

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
      // callback(newSkill) // TODO: other way to do this
    },
    async deleteSkill(deletedSkill: Skill) {
      await instance
        .delete(`skills/${deletedSkill.id}/`)
        .then(() => {
          const index = this.skills.findIndex(
            (skill) => skill.id === deletedSkill.id
          )
          this.skills.splice(index, 1)
        })
        .catch(() => console.log('Failed to delete'))
    },

    /*
     * PROJECT TODO: move to a project store once that exists
     */
    submitProject(
      projectName: string,
      projectURL: string,
      partnerName: string,
      coaches: User[]
    ) {
      const data: Project = {
        name: projectName,
        partner_name: partnerName,
        extra_info: projectURL,
        required_skills: [],
        coaches: [],
        suggested_students: []
      }

      // filter out the used skills
      for (const skill of this.skills) {
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
      coaches.forEach((coach) => data.coaches.push(coach.url))

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

      // callback()
    },
  },
})
