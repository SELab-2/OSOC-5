import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { Student, TempStudent } from '../models/Student'
import { User } from '../models/User'
import { Skill, ProjectSkill, TempProjectSkill } from '../models/Skill'
import { ProjectSuggestion } from '../models/ProjectSuggestion'
import { Project, TempProject } from '../models/Project'
import { useCoachStore } from './useCoachStore'
import { Either, left, right } from '../models/Either'

interface State {
  projects: Array<Project>
  isLoadingProjects: boolean
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
          skill: await instance.get(student.skill).then(res => res.data) as Skill,
          reason: student.reason
        }
        newStudents.push(newStudent)
      }
      return newStudents
    },
    async removeSuggestion(project: Project, suggestion: ProjectSuggestion) {
      return instance.post(`projects/${project.id}/remove_student/`, {
        student: suggestion.student.url,
        skill: suggestion.skill.url
      })
    },
    async addSuggestion(projectId: number, studentUrl: URL, skillUrl: URL, reason: string) {
      return await instance.post(`projects/${projectId}/suggest_student/`, {
        student: studentUrl,
        skill: skillUrl,
        reason: reason
      })
    },
    async getSkill(skill: TempProjectSkill): Promise<ProjectSkill> {
      let { data } = await instance.get<Skill>(skill.skill)
      return {
        amount: skill.amount,
        comment: skill.comment,
        skill: data
      }
    },
    async getProject(project: TempProject) {
      let coaches: Array<User> = await Promise.all(
        project.coaches.map(coach => useCoachStore().getUser(coach))
      )
      
      let skills: Array<Skill|any> = await Promise.all(
        project.requiredSkills.map(skill => this.getSkill(skill))
      )
      
      let students: Array<ProjectSuggestion> = await this.fetchSuggestedStudents(project.suggestedStudents)
      
      // Is added to projects here because we do not want to await on each project.
      this.projects = this.projects.concat([new Project(
          project.name,
          project.partnerName,
          project.extraInfo,
          skills,
          coaches,
          students,
          project.id
        )
      ])
      
    },
    async loadProjects() {
      this.isLoadingProjects = true
      try {
        let { data } = await instance
          .get<TempProject[]>('projects/')
        
        // for (let project of data) {
        //   this.projects = this.projects.concat([await this.getProject(project)])
        //   // this.projects.push(await this.getProject(project))
        // }
        // this.projects = this.projects.slice(1)
        data.forEach(p => this.getProject(p))
      } catch (error) {
        console.log(error)
        this.isLoadingProjects = false
      }
    }
  },
})
