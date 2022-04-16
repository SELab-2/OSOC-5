import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { Student, TempStudent } from '../models/Student'
import { User } from '../models/User'
import { Skill, ProjectSkillInterface, ProjectSkill, TempProjectSkill } from '../models/Skill'
import { ProjectSuggestionInterface, ProjectSuggestion } from '../models/ProjectSuggestion'
import { Project, TempProject } from '../models/Project'
import { useCoachStore } from './useCoachStore'

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
    async fetchSuggestedStudents(
      students: TempStudent[]
    ): Promise<ProjectSuggestionInterface[]> {
      const newStudents: ProjectSuggestionInterface[] = []
      for (const student of students) {
        const newStudent = new ProjectSuggestion({
          student: (await instance.get(student.student)).data as Student,
          coach: (await instance.get(student.coach)).data as User,
          skill: (await instance.get(student.skill)).data as Skill,
          reason: student.reason,
        })
        newStudents.push(newStudent)
      }
      return newStudents
    },
    async removeSuggestion(project: Project, suggestion: ProjectSuggestionInterface) {
      return instance.post(`projects/${project.id}/remove_student/`, {
        student: suggestion.student.url,
        skill: suggestion.skill.url,
      })
    },
    async addSuggestion(
      projectId: number,
      studentUrl: string,
      skillUrl: string,
      reason: string
    ) {
      return await instance.post(`projects/${projectId}/suggest_student/`, {
        student: studentUrl,
        skill: skillUrl,
        reason: reason,
      })
    },
    async getSkill(skill: TempProjectSkill): Promise<ProjectSkill> {
      const { data } = await instance.get<Skill>(skill.skill)
      return new ProjectSkill(skill.amount, skill.comment, new Skill(data))
    },
    async getProject(project: TempProject) {
      const coaches: Array<User> = await Promise.all(
        project.coaches.map((coach) => useCoachStore().getUser(coach))
      )

      const skills: Array<ProjectSkillInterface> = await Promise.all(
        project.requiredSkills.map((skill) => this.getSkill(skill))
      )

      const students: Array<ProjectSuggestionInterface> =
        await this.fetchSuggestedStudents(project.suggestedStudents)

      // Is added to projects here because we do not want to await on each project.
      this.projects = this.projects.concat([
        new Project(
          project.name,
          project.partnerName,
          project.extraInfo,
          project.id,
          skills,
          coaches,
          students
        ),
      ])
    },
    async loadProjects() {
      this.isLoadingProjects = true
      try {
        const { data } = await instance.get<TempProject[]>('projects/')
        this.projects = data.map(
          (p) => new Project(p.name, p.partnerName, p.extraInfo, p.id)
        )
        data.forEach(async (project, i) => {
          const coaches: Array<User> = await Promise.all(
            project.coaches.map((coach) => useCoachStore().getUser(coach))
          )

          const skills: Array<ProjectSkillInterface> = await Promise.all(
            project.requiredSkills.map((skill) => this.getSkill(skill))
          )

          const students: Array<ProjectSuggestionInterface> =
            await this.fetchSuggestedStudents(project.suggestedStudents)

          this.projects[i].coaches = coaches
          this.projects[i].requiredSkills = skills
          this.projects[i].suggestedStudents = students
        })
        // for (let [i, project] of data.entries()) {
        //
        //   // this.projects = [...this.projects]
        // }
        // for (let project of data) {
        //   this.projects = this.projects.concat([await this.getProject(project)])
        //   // this.projects.push(await this.getProject(project))
        // }
        // this.projects = this.projects.slice(1)
        // data.forEach(p => this.getProject(p))
      } catch (error) {
        console.log(error)
        this.isLoadingProjects = false
      }
    },
  },
})
