import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { Student } from '../models/Student'
import { User } from '../models/User'
import { Skill } from '../models/Skill'
import { ProjectSuggestion } from '../models/ProjectSuggestion'
import { Project } from '../models/Project'

interface State {
  projects: Array<Project>
  isLoadingProjects: boolean
}

interface TempStudent {
  student: string
  coach: string
  role: string
  reason: string
}

interface TempProject {
  id: number
  name: string
  suggestedStudents: TempStudent[]
  partnerName: string,
  extraInfo: string,
  coaches: string[]
  requiredSkills: {
    amount: number
    skill: string
  }[]
}

export const useProjectStore = defineStore('project', {
  state: (): State => ({
    projects: [],
    isLoadingProjects: false,
  }),
  actions: {
    async fetchSuggestedStudents(students: TempStudent[]): Promise<ProjectSuggestion[]> {
      var newStudents: ProjectSuggestion[] = []
      for (const student of students) {
        var newStudent: ProjectSuggestion = {
          student: await instance.get(student.student).then(res => res.data) as Student,
          coach: await instance.get(student.coach).then(res => res.data) as User,
          skill: await instance.get(student.role).then(res => res.data) as Skill,
          reason: student.reason
        }
        newStudents.push(newStudent)
      }
      return newStudents
    },
    async removeSuggestion(project: Project, suggestion: ProjectSuggestion) {
      return instance.post(`projects/${project.id}/remove_student/`, {
        student: suggestion.student.url,
        role: suggestion.skill.url
      })
    },
    async addSuggestion(projectId: number, studentUrl: URL, skillUrl: URL, reason: string) {
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
      var projects = convertObjectKeysToCamelCase(data as any).data as TempProject[]
      var newProjects: Project[] = []
      for (const project of projects) {
        
        const data = await Promise.all(
          project.coaches.map((coach) => {
            return instance.get(coach)
          })
        )

        const data2 = await Promise.all(
          project.requiredSkills.map(skill => {
            return instance.get(skill.skill)
          })
        )
        
        const fetchedProj: Project = {
          id: project.id,
          name: project.name,
          partnerName: project.partnerName,
          extraInfo: project.extraInfo,
          coaches: (convertObjectKeysToCamelCase(data as any) as any).map((res: any): User => res.data) as any as User[],
          suggestedStudents: convertObjectKeysToCamelCase(await this.fetchSuggestedStudents(project.suggestedStudents) as any) as unknown as ProjectSuggestion[],
          requiredSkills: project.requiredSkills.map((skill, j) => {
            return {
              skill: convertObjectKeysToCamelCase(data2[j].data) as unknown as Skill,
              amount: skill.amount
            }
          })
          
        }
        newProjects.push(fetchedProj)
      }
      this.projects = newProjects

    },
  },
})
