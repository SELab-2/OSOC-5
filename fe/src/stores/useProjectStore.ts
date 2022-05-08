import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { Student } from '../models/Student'
import {
  TempProjectSuggestion,
  NewProjectSuggestion,
} from '../models/ProjectSuggestion'
import { User } from '../models/User'
import {
  Skill,
  ProjectSkillInterface,
  ProjectSkill,
  TempProjectSkill,
  ProjectTableSkill,
} from '../models/Skill'
import {
  ProjectSuggestionInterface,
  ProjectSuggestion,
} from '../models/ProjectSuggestion'
import { Project, TempProject } from '../models/Project'
import { useCoachStore } from './useCoachStore'
import { useStudentStore } from './useStudentStore'
import { useSkillStore } from './useSkillStore'
import { convertObjectKeysToSnakeCase } from '../utils/case-conversion'

interface State {
  projects: Array<Project>
  isLoadingProjects: boolean
  projectName: string
  projectPartnerName: string
  projectLink: string
  filterCoaches: string
  selectedCoaches: Array<User>
  projectFilter: string
}

export const useProjectStore = defineStore('project', {
  state: (): State => ({
    projects: [],
    isLoadingProjects: false,
    projectName: '',
    projectPartnerName: '',
    projectLink: '',
    filterCoaches: '',
    selectedCoaches: [],
    projectFilter: '',
  }),
  actions: {
    async getConflictingProjects() {
      const studentStore = useStudentStore()

      const conflicts = (
        await instance.get('projects/get_conflicting_projects')
      ).data as Array<{ student: string; projects: Array<string> }>
      const resConflicts = []
      for (const conflict of conflicts) {
        const student = await studentStore.getStudent(conflict.student)
        const projects = await Promise.all(
          conflict.projects.map(
            async (project: string) => await this.getOrFetchProject(project)
          )
        )

        resConflicts.push({ student, projects })
      }

      return resConflicts
    },
    async fetchSuggestedStudents(
      students: TempProjectSuggestion[]
    ): Promise<ProjectSuggestionInterface[]> {
      const newStudents: ProjectSuggestionInterface[] = []
      for (const student of students) {
        const newStudent = new ProjectSuggestion({
          student: (await instance.get(student.student)).data as Student,
          coach: await useCoachStore().getUser(student.coach),
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
            async (url) => await coachStore.loadUser(url as unknown as string)
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
        const { results } = (
          await instance.get<{ results: TempProject[] }>(
            `projects/?search=${this.projectFilter}`
          )
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
        console.log(error)
      } finally {
        this.isLoadingProjects = false
      }
    },
    async receiveSuggestion({
      project_id,
      reason,
      coach,
      student,
      skill,
    }: {
      project_id: string
      reason: string
      coach: { id: number; firstName: string; lastName: string; url: string }
      student: string
      skill: string
    }) {
      const projectId = Number.parseInt(project_id)
      const project = this.projects.filter(({ id }) => id === projectId)[0]

      const alreadyExists = project.suggestedStudents?.some(
        (suggestion) =>
          suggestion.skill.url === skill && suggestion.student.url === student
      )

      if (!alreadyExists) {
        const studentStore = useStudentStore()
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
      }
    },
    removeReceivedSuggestion({
      skill,
      student,
      project_id,
    }: {
      skill: string
      student: string
      project_id: string
    }) {
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
        )
          project.suggestedStudents?.splice(suggestionIndex, 1)
      }
    },
    submitProject(
      skills: Array<ProjectTableSkill>,
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      callback: any
    ) {
      const skillsList: Array<TempProjectSkill> = []

      // filter out the used skills
      for (const skill of skills) {
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
      this.selectedCoaches.forEach((coach: User) => coachList.push(coach.url))

      const data = {
        name: this.projectName,
        partnerName: this.projectPartnerName,
        extraInfo: this.projectLink,
        requiredSkills: skillsList,
        coaches: coachList,
      }

      // POST request to make a project
      instance
        .post('projects/', convertObjectKeysToSnakeCase(data))
        .then((response) => {
          this.loadProjects()

          // clear fields when project is made successfully
          this.isLoadingProjects = false
          this.projectName = ''
          this.projectPartnerName = ''
          this.projectLink = ''
          this.filterCoaches = ''
          this.selectedCoaches = []
          useSkillStore().loadSkills()

          // this.projects.push({
          //   name: response['data']['name'],
          //   id:  response['data']['id'],
          //   partnerName: response['data']['partner_name'],
          //   extraInfo: response['data']['extra_info'],
          //   requiredSkills: response['data']['required_skills'],
          //   coaches: response['data']['coaches'],
          // });

          callback(true)
        })
        .catch(function (error) {
          console.log(error)
          callback(false)
        })
    },
    resolveConflict() {},
    editProject(project: Project) {
      this.projectName = project.name
      this.projectPartnerName = project.partnerName
      this.projectLink = project.extraInfo
      this.selectedCoaches = []
      // skills
    },
  },
})
