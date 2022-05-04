import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { Student, TempStudent } from '../models/Student'
import { TempProjectSuggestion } from '../models/ProjectSuggestion'
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
      for (const student of students) {
        const newStudent = new ProjectSuggestion({
          student: (await instance.get(student.student)).data as Student,
          coach: (await useCoachStore().getUser(student.coach)),
          skill: (await instance.get(student.skill)).data as Skill,
          reason: student.reason,
        })
        newStudents.push(newStudent)
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
      return await instance.post(`projects/${projectId}/suggest_student/`, {
        student: studentUrl,
        skill: skillUrl,
        reason: reason,
      })
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
    // NOTE: this may be broken.

    /**
     * Gets a project
     * @param project the project to get
     */
    async getProject(project: TempProject) {
      console.log("Loading")
      const coaches: Array<User> = await Promise.all(
        project.coaches.map((coach) =>
          useCoachStore().getUser(coach)
        )
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
    /**
     * Loads the projects
     */
    async loadProjects() {
      this.isLoadingProjects = true
      try {
        const { results } = (await instance.get<{results: TempProject[]}>('projects/')).data
        this.projects = results.map(
          (p) => new Project(p.name, p.partnerName, p.extraInfo, p.id)
        )
        results.forEach(async (project, i) => {
          const coaches: Array<User> = await Promise.all(
            project.coaches.map((coach) =>
              useCoachStore().getUser(coach)
            )
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
    /**
     * Called when we recieve a suggestion from the websocket
     * @param param0 object received from the websocket
     */
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

        project.suggestedStudents?.push({
          student: studentObj,
          coach: coachObj,
          skill: skillObj,
          reason,
        })
      }
    },
    /**
     * Called when we receive a remove suggestion from the websocket
     * @param param0 object received from the websocket
     */
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
          suggestionIndex &&
          suggestionIndex !== -1 &&
          project.suggestedStudents &&
          suggestionIndex < project.suggestedStudents.length &&
          project.suggestedStudents[suggestionIndex].student.url === student
        )
          project.suggestedStudents?.splice(suggestionIndex, 1)
      }
    },
    /**
     * TODO
     * @param skills 
     * @param callback 
     */
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
          this.isLoadingProjects=  false
          this.projectName= ''
          this.projectPartnerName= ''
          this.projectLink= ''
          this.filterCoaches=''
          this.selectedCoaches= []
          useSkillStore().loadSkills()

          callback(true)
        })
        .catch(function (error) {
          callback(false)
        })
    },
    editProject(project: Project){
      this.projectName= project.name
      this.projectPartnerName= project.partnerName
      this.projectLink= project.extraInfo
      this.selectedCoaches= []
      // skills
    }
  },
})
