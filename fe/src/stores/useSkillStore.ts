import { defineStore } from 'pinia'
import { instance } from '../utils/axios'

import { ProjectTableSkill, Skill, TempProjectSkill, ProjectSkill } from '../models/Skill'
import { User } from '../models/User'

interface State {
  skills: Array<Skill>
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
      const { data } = await instance.get<Skill>(url)

      // Check again if not present, it could be added in the meantime.
      const skill2 = this.skills.find((skill) => skill.url === url)
      if (skill2) return skill2

      const newSkill = new Skill(data)
      this.skills.push(newSkill)
      return newSkill
    },
    /*
     * SKILLS
     */
    async loadSkills() {
      const { results } = (await instance.get<{ results: Skill[] }>('skills/?page_size=500')).data
      this.skills = results.map(skill => new Skill(skill.name, skill.id, skill.color, skill.url))
    },
    
    async loadNext(index: number, done: Function, filters: Object) {
      if (index === 1) this.skills = []
      
      const { results, next } = (await instance.get<{ results: Skill[], next: string }>(`skills/?page=${index}`, { params: filters })).data
      
      this.skills.push(...results.map(s => new Skill(s)))
      done(next === null)
    },

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async addSkill(skill: Skill, callback: Function) {
      try {
        const { data } = await instance.post<Skill>('skills/', {
          name: skill.name,
          color: skill.color,
        })
        this.skills.push(data)
        callback(true)
      } catch (e) {
        callback(false)
      }
    },
    
    async updateSkill(skill: Skill, callback: Function) {
      try {
        await instance.patch(`skills/${skill.id}/`, skill)
      } catch(e) {
        // Should put the previous value back
        callback()
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
    async setSkills(projectSkills: TempProjectSkill[]) {
      // first load all the existing skills back into the store
      await this.loadSkills()
      // now go over each of the skills that the project contains and
      // fill in the amount and comment
      for (const projectSkill of projectSkills) {
        for (const skill of this.skills) {
          if (skill.url === projectSkill.skill) {
            // this means u found match
            // console.log("match " + skill.url)
            skill.amount = projectSkill.amount
            skill.comment = projectSkill.comment
          }
        }
      }
    },
  },
})
