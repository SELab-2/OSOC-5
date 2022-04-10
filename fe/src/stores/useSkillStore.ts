import { defineStore } from 'pinia'
import { instance } from '../utils/axios'

import { ProjectSkill, ProjectTableSkill, Skill } from '../models/Skill'

interface State {
  skills: Array<ProjectTableSkill>
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
          // set the skill of the store
          for (const skill of data as Skill[]) {
            this.skills.push({
              name: skill.name,
              amount: 0,
              url: skill.url,
              color: skill.color,
              id: skill.id,
              comment: '',
            })
          }

          // turn of the loading animation
          this.isLoadingSkills = false
        })
        .catch((error) => {
          console.log(error)
          return (this.isLoadingSkills = false)
        })
    },

    async addSkill(newSkillName: string, color: string, callback: any) {
      // start the loading animation
      this.isLoadingSkills = true

      // Process the new skill
      console.log(`Adding new skill: ${newSkillName}.`)


      instance
        .post('skills/', {
          'name': newSkillName,
          'color': color,
        })
        .then((response) => {
          console.log(response['data'])

          // ON SUCCESS ADD THIS TO THE LOCAL STORE
          this.skills.push({
            name: response['data']['name'],
            amount: 0,
            url: response['data']['url'],
            color: response['data']['color'],
            id: response['data']['id'],
            comment: '',
          })
          console.log(this.skills)

          // turn of the loading animation
          this.isLoadingSkills = false
          // When finished run the callback so the popup closes.
          callback(true)
        })
        .catch(function (error) {
          console.log(error)
          callback(false)
        })
    },
    async deleteSkill(deletedSkillId: number) {
      // delete in database
      await instance
        .delete(`skills/${deletedSkillId}/`)
        .then(() => {
          // delete locally
          const index = this.skills.findIndex(
            (skill) => skill.id === deletedSkillId
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
      coaches: Array<string>,
      callback: any
    ) {
      const skillsList: Array<ProjectSkill> = []

      // filter out the used skills
      for (const skill of this.skills) {
        if (skill.amount > 0) {
          skillsList.push({
            skill: skill.url,
            amount: skill.amount,
            comment: skill.comment,
          })
        }
      }

      const coachList: Array<string> = []

      // add the selected coaches to data object
      coaches.forEach((coach) => coachList.push(coach))

      const data = {
        name: projectName,
        partner_name: partnerName,
        extra_info: projectURL,
        required_skills: skillsList,
        coaches: coachList,
      }

      // POST request to make a project
      instance
        .post('projects/', data)
        .then(function (response) {
          console.log(response)
          callback(true)
        })
        .catch(function (error) {
          console.log(error)
          callback(false)
        })
    },
  },
})