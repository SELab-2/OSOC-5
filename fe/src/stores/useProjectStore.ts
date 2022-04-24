import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { Student, TempStudent } from '../models/Student'
import { User } from '../models/User'
import {
  Skill,
  ProjectSkillInterface,
  ProjectSkill,
  TempProjectSkill,
} from '../models/Skill'
import {
  ProjectSuggestionInterface,
  ProjectSuggestion,
} from '../models/ProjectSuggestion'
import { Project, TempProject } from '../models/Project'
import { useCoachStore } from './useCoachStore'
import { useStudentStore } from './useStudentStore'
import { useSkillStore } from './useSkillStore'

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
    async getConflictingProjects() {
      const studentStore = useStudentStore()

      const { data } = await instance.get('projects/get_conflicting_projects')
      const conflicts = new Map()
      for (const conflict of Object.entries(data.conflicts)) {
        console.log(conflict)
        const student = await studentStore.getStudent(conflict[0])
        const projects = await Promise.all(
          (conflict[1] as string[]).map(
            async (project: string) => await this.getOrFetchProject(project)
          )
        )
        conflicts.set(student, projects)
      }

      return conflicts
    },
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
    async removeSuggestion(
      project: Project,
      suggestion: ProjectSuggestionInterface
    ) {
      return instance.post(`projects/${project.id}/remove_student/`, {
        student: suggestion.student.url,
        skill: suggestion.skill.url,
        coach: suggestion.coach.url,
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
    async getOrFetchProject(url: string) {
      const splittedUrl = url.split('/')
      const id = Number.parseInt(splittedUrl[splittedUrl.length - 2])

      const localPoject = this.projects.filter(
        (project) => project.id === id
      )[0]

      if (localPoject) return localPoject

      const { data } = await instance.get<Project>(`projects/${id}`)
      const coachStore = useCoachStore()

      if (data.coaches)
        data.coaches = await Promise.all(
          data.coaches.map(
            async (url) => await coachStore.getUser(url as unknown as string)
          )
        )

      return data
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
    async receiveSuggestion({
      student_id,
      skill_id,
      project_id,
      reason,
      coach,
      student,
      skill,
    }: {
      student_id: number
      skill_id: number
      project_id: number
      reason: string
      coach: string
      student: string
      skill: string
    }) {
      const project = this.projects.filter(({ id }) => id === project_id)[0]
      const alreadyExists = project.suggestedStudents?.some(
        (suggestion) =>
          suggestion.skill.id === skill_id &&
          suggestion.student.id === student_id
      )

      if (!alreadyExists) {
        const studentStore = useStudentStore()
        const coachStore = useCoachStore()
        const skillStore = useSkillStore()

        const studentObj = await studentStore.getStudent(student)
        const coachObj = await coachStore.getUser(coach)
        const skillObj = await skillStore.getSkill(skill)

        project.suggestedStudents?.push({
          student: studentObj,
          coach: coachObj,
          skill: skillObj,
          reason,
        })
      }
    },
    removeReceivedSuggestion({
      skill,
      student,
      project_id,
    }: {
      skill: string
      student: string
      project_id: number
    }) {
      const project = this.projects.filter(({ id }) => id === project_id)[0]

      if (project) {
        const suggestionIndex = project.suggestedStudents?.findIndex(
          (s) => s.student.url === student && s.skill.url === skill
        )

        if (
          suggestionIndex &&
          suggestionIndex !== -1 &&
          project.suggestedStudents &&
          suggestionIndex < project.suggestedStudents.length &&
          project.suggestedStudents[suggestionIndex].student.url === student
        )
          project.suggestedStudents?.splice(suggestionIndex, 1)
      }
    },
  },
})
