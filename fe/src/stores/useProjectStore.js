import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    isLoadingProjects: false,
  }),
  actions: {
    async fetchSuggestedStudents(students) {
      for (var [i, student] of students.entries()) {
        student.student = await instance.get(student.student).then(res => res.data)
        student.coach = await instance.get(student.coach).then(res => res.data)
        student.role = await instance.get(student.role).then(res => res.data)
        students[i] = student
      }
      return students
    },
    async removeSuggestion(project, suggestion) {
      return instance.post(`projects/${project.id}/remove_student/`, {
        student: suggestion.student.url,
        role: suggestion.role.url
      })
    },
    async addSuggestion(projectId, studentUrl, skillUrl, reason) {
      return await instance.post(`projects/${projectId}/suggest_student/`, {
        student: studentUrl,
        role: skillUrl,
        reason: reason
      })
    },
    async loadProjects() {
      this.isLoadingProjects = true
      let data = await instance
        .get('projects/')
        .catch(() => (this.isLoadingProjects = false))
        
      this.isLoadingProjects = false
      var projects = convertObjectKeysToCamelCase(data).data

      for (var [i, project] of projects.entries()) {
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
        
        var students = await this.fetchSuggestedStudents(project.suggestedStudents)
        students = convertObjectKeysToCamelCase(students)
        project.suggestedStudents = students
        projects[i] = project
        console.log("parsed")
      }
      
      this.projects = projects

      console.log(this.projects)
    },
  },
})
