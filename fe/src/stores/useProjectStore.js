import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    isLoadingProjects: false,
  }),
  actions: {
    async loadProjects() {
      this.isLoadingProjects = true
      let data = await instance
        .get('projects/')
        .catch(() => (this.isLoadingProjects = false))
        
      this.isLoadingProjects = false
      this.projects = convertObjectKeysToCamelCase(data).data

      for (var [i, project] of this.projects.entries()) {
        const data = await Promise.all(
          project.coaches.map((coach) => {
            return instance.get(coach)
          })
        )
        project.coaches = convertObjectKeysToCamelCase(data).map(
          (res) => res.data
        )

        const data2 = await Promise.all(
          project.requiredSkills.map((skill) => {
            return instance.get(skill.skill)
          })
        )

        project.requiredSkills = project.requiredSkills.map((skill, j) => {
          skill.skill = convertObjectKeysToCamelCase(data2[j].data)
          return skill
        })
        this.projects[i] = project
        console.log("parsed")
      }

      console.log(this.projects)
    },
  },
})
