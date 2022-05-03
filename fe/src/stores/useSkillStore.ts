import { defineStore } from 'pinia'
import { instance } from '../utils/axios'

import { ProjectTableSkill, Skill } from '../models/Skill'
import { User } from '../models/User'

interface State {
  skills: Array<ProjectTableSkill>
  isLoadingSkills: boolean
  popupName: string
  popupColor: string
  popupID: number
}

export const useSkillStore = defineStore('skills', {
  state: (): State => ({
    skills: [],
    isLoadingSkills: false,
    popupName: '',
    popupColor: '',
    popupID: -1,
  }),
  actions: {
    async getSkill(url: string): Promise<Skill> {
      const skill = this.skills.find((skill) => skill.url === url)
      if (skill) return skill
      const { data } = await instance.get<ProjectTableSkill>(url)

      // Check again if not present, it could be added in the meantime.
      const skill2 = this.skills.find((skill) => skill.url === url)
      if (skill2) return skill2

      const newSkill = new Skill(data)
      this.skills.push({
        name: newSkill.name,
        amount: 0,
        url: newSkill.url,
        color: newSkill.color,
        id: newSkill.id,
        comment: '',
      })
      return newSkill
    },
    /*
     * SKILLS
     */
    async loadSkills() {
      // start the loading animation
      this.isLoadingSkills = true
      this.skills = []
      // console.log('LOAD SKILLS')
      instance
        .get('skills/?page_size=500')
        .then(({ data }) => {
          // set the skill of the store
          for (const skill of data['results'] as Skill[]) {
            this.skills.push({
              name: skill.name,
              amount: 0,
              url: skill.url,
              color: skill.color,
              id: skill.id,
              comment: '',
            })
          }
        })
        .catch((error) => {
          console.log(error)
        })
        .finally(() => (this.isLoadingSkills = false))
    },

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async addSkill(callback: any) {
      // Process the new skill
      console.log(`Adding new skill: ${this.popupName}.`)
      if (
        this.popupName &&
        this.popupName.length > 0 &&
        this.popupColor.length > 0
      ) {
        if (this.popupID >= 0) {
          // skill already exists so we update it
          instance
            .put(`skills/${this.popupID}/`, { color: this.popupColor })
            .then(() => callback(0))
            .catch(() => callback(1))
        } else {
          // make new skill
          instance
            .post('skills/', {
              name: this.popupName,
              color: this.popupColor,
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
              // When finished run the callback so the popup closes.
              callback(0)
            })
            .catch((error) => {
              this.isLoadingSkills = false
              console.log(error)
              callback(1)
            })
        }
      } else {
        callback(2)
      }
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async deleteSkill(deletedSkillId: number, callback: any) {
      // delete in database
      await instance
        .delete(`skills/${deletedSkillId}/`)
        .then(() => {
          // delete locally
          const index = this.skills.findIndex(
            (skill) => skill.id === deletedSkillId
          )
          this.skills.splice(index, 1)
          callback(true)
        })
        .catch((error) => {
          console.log(error)
          callback(false)
        })
    },
  },
})
