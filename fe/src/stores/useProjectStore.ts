import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { Student } from '../models/Student'
import {
  TempProjectSuggestion,
  NewProjectSuggestion,
} from '../models/ProjectSuggestion'
import { User, UserInterface } from '../models/User'
import {
  ProjectSkill,
  ProjectSkillInterface,
  Skill,
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
import { convertObjectKeysToCamelCase, convertObjectKeysToSnakeCase } from '../utils/case-conversion'

interface State {
  projects: Array<Project>
  
  // Flag so projectlist can determine if it should reset the pagination and reload all the projects or not.
  // Is used e.g. when a conflict is resolved, or a project is created/updated.
  shouldRefresh: Boolean
}

export const useProjectStore = defineStore('project', {
  state: (): State => ({
    projects: [],
    shouldRefresh: false
  }),
  actions: {
    /**
     * Fetches the suggested students
     * @param students the students to fetch
     * @returns the fetched students
     */
    async fetchSuggestedStudents(
      students: TempProjectSuggestion[]
    ): Promise<ProjectSuggestionInterface[]> {
      const newStudents: ProjectSuggestionInterface[] = []
      if (students) {
        for (const student of students) {
          const newStudent = new ProjectSuggestion({
            student: (await instance.get(student.student)).data as Student,
            coach: await useCoachStore().getUser(student.coach),
            skill: (await instance.get(student.skill)).data as Skill,
            reason: student.reason,
          })
          newStudents.push(newStudent)
        }
      }
      return newStudents
    },
    /**
     * Removes a suggestion from a project
     * @param project the associated project
     * @param suggestion the suggestion which needs to be removed
     * @returns data returned by the back-end
     */
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
    /**
     * Adds a suggestion to a project
     * @param projectId the id of the project for which a suggestion is added
     * @param studentUrl url of the student
     * @param skillUrl url of the skill
     * @param reason the reason why we made this suggestion
     * @returns data returned by the back-end
     */
    async addSuggestion(
      projectId: number,
      studentUrl: string,
      skillUrl: string,
      reason: string
    ) {
      const response = await instance.post(
        `projects/${projectId}/suggest_student/`,
        {
          student: studentUrl,
          skill: skillUrl,
          reason: reason,
        }
      )

      return response
    },
    /**
     * Gets a skill
     * @param skill the skill which we want to get
     * @returns the fetched skill
     */
    async getSkill(skill: TempProjectSkill): Promise<ProjectSkill> {
      const { data } = await instance.get<Skill>(skill.skill)
      return new ProjectSkill(skill.amount, skill.comment, new Skill(data))
    },
    /**
     * Gets a project
     * @param project the project to get
     */
    async getProject(id: number): Promise<Project> {

      const project = (await instance.get<TempProject>(`projects/${id}/`)).data
      const coaches: Array<User> = await Promise.all(
        project.coaches.map((coach) => useCoachStore().getUser(coach))
      )

      const skills: Array<ProjectSkillInterface> = await Promise.all(
        project.requiredSkills.map((skill) => this.getSkill(skill))
      )

      const students: Array<ProjectSuggestionInterface> =
        await this.fetchSuggestedStudents(project.suggestedStudents)

      // Is added to projects here because we do not want to await on each project.
      return new Project(
          project.name,
          project.partnerName,
          project.extraInfo,
          project.id,
          skills,
          coaches,
          students
        )
      
    },
    /**
     * Loads the projects
     */
    async loadProjects() {
      try {
        const { results } = (
          await instance.get<{ results: TempProject[] }>('projects/')
        ).data
        this.projects = results.map(
          (p) => new Project(p.name, p.partnerName, p.extraInfo, p.id)
        )
        results.forEach(async (project, i) => {
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
        // console.log(error)
      }
    },
    async loadNext(index: number, done: Function, filters: Object) {
      // Remove all the data when the first page is requested.
      if (index === 1) this.projects = []

      const { results, next } = (
        await instance.get<{ results: TempProject[]; next: string }>(
          `projects/?page=${index}`,
          { params: filters }
        )
      ).data

      let base = this.projects.length

      this.projects = [
        ...this.projects,
        ...results.map(
          (p) => new Project(p.name, p.partnerName, p.extraInfo, p.id)
        ),
      ]

      results.forEach(async (project, i) => {
        const coaches: Array<User> = await Promise.all(
          project.coaches.map((coach) => useCoachStore().getUser(coach))
        )

        const skills: Array<ProjectSkillInterface> = await Promise.all(
          project.requiredSkills.map((skill) => this.getSkill(skill))
        )

        const students: Array<ProjectSuggestionInterface> =
          await this.fetchSuggestedStudents(project.suggestedStudents)

        this.projects[base + i].coaches = coaches
        this.projects[base + i].requiredSkills = skills
        this.projects[base + i].suggestedStudents = students
      })
      // If next is null, we are at the end of the results.
      // We can signal this to q-infinite-scroll by returning done(true)
      done(next === null)
    },
    /**
     * Called when we recieve a suggestion from the websocket
     * @param param0 object received from the websocket
     */
    async receiveSuggestion(
      {
        project_id,
        reason,
        coach,
        student,
        skill,
      }: {
        project_id: string
        reason: string
        coach: UserInterface
        student: string
        skill: string
      },
      onProject: string
    ) {
      const projectId = Number.parseInt(project_id)
      const project = this.projects.filter(({ id }) => id === projectId)[0]

      const alreadyExists = project.suggestedStudents?.some(
        (suggestion) =>
          suggestion.skill.url === skill && suggestion.student.url === student
      )

      const studentStore = useStudentStore()

      if (alreadyExists) {
        if (onProject === 'false')
          studentStore.students = studentStore.students.filter(
            ({ url }) => url !== student
          )

        return
      }

      const coachStore = useCoachStore()
      const skillStore = useSkillStore()

      const studentObj = await studentStore.getStudent(student)
      const coachObj = await coachStore.getUser(coach)
      const skillObj = await skillStore.getSkill(skill)

      project.suggestedStudents?.push(
        new NewProjectSuggestion(
          {
            student: studentObj,
            coach: coachObj,
            skill: skillObj,
            reason,
          },
          true
        )
      )

      if (onProject === 'false')
        studentStore.students = studentStore.students.filter(
          ({ url }) => url !== student
        )
      else if (
        onProject === 'true' &&
        !studentStore.students.some(({ url }) => url === student)
      )
        await studentStore.getStudent(student)

      // Remove the "New" badge from the new suggestion after a short period.
      setTimeout(
        () =>
          ((
            project.suggestedStudents?.find(
              (s) =>
                s.student.url === studentObj.url &&
                s.coach.url === coachObj.url &&
                s.skill.url === skillObj.url
            ) as NewProjectSuggestion
          ).fromWebsocket = false),
        5000
      )
    },
    /**
     * Called when we receive a remove suggestion from the websocket
     * @param param0 object received from the websocket
     */
    async removeReceivedSuggestion(
      {
        skill,
        student,
        project_id,
      }: {
        skill: string
        student: string
        project_id: string
      },
      onProject: string
    ) {
      const projectId = Number.parseInt(project_id)
      const project = this.projects.filter(({ id }) => id === projectId)[0]

      if (project) {
        const suggestionIndex = project.suggestedStudents?.findIndex(
          (s) => s.student.url === student && s.skill.url === skill
        )
        if (
          suggestionIndex !== undefined && // !== undefined must be written here, otherwise suggestionIndex === 0 will fail.
          suggestionIndex !== -1 &&
          project.suggestedStudents &&
          suggestionIndex < project.suggestedStudents.length &&
          project.suggestedStudents[suggestionIndex].student.url === student
        ) {
          const studentStore = useStudentStore()

          if (onProject === 'true')
            studentStore.students = studentStore.students.filter(
              ({ url }) => url !== student
            )
          else if (
            onProject === 'false' &&
            !studentStore.students.some(({ url }) => url === student)
          )
            await studentStore.getStudent(student)

          project.suggestedStudents?.splice(suggestionIndex, 1)
        }
      }
    },

    async addProject(project: Project) {
      try {
        const mappedProject = {
          name: project.name,
          partnerName: project.partnerName,
          extraInfo: project.extraInfo,
          requiredSkills: project.requiredSkills?.map(s => {
            return {
              amount: s.amount,
              comment: s.comment,
              skill: s.skill.url
            }
          }),
          coaches: project.coaches?.map(c => c.url),					
        }
        await instance.post('projects/', convertObjectKeysToSnakeCase(mappedProject))
        return true
      } catch (error) {
        return false
      }
    },
    async updateProject(project: Project, id: number) {
      try {
        const mappedProject = {
          name: project.name,
          partnerName: project.partnerName,
          extraInfo: project.extraInfo,
          requiredSkills: project.requiredSkills?.map(s => {
            return {
              amount: s.amount,
              comment: s.comment,
              skill: s.skill.url
            }
          }),
          coaches: project.coaches?.map(c => c.url),					
        }
        await instance.patch(`projects/${id}/`, convertObjectKeysToSnakeCase(mappedProject))
        return true
      } catch (error) {
        return false
      }
    },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async deleteProject(id: number, callback: any) {
      await instance
        .delete(`projects/${id}/`)
        .then(() => {
          callback(true)
        })
        .catch(() => {
          callback(false)
        })
    },
  },
})
