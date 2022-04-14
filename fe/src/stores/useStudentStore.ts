import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { User } from '../models/User'
import { Student } from '../models/Student'
import { Skill } from '../models/Skill'
import { useCoachStore } from './useCoachStore'

interface State {
  search: string
  alumni: string
  decision: string
  byMe: boolean
  onProject: boolean
  skills: Array<Skill>
  coaches: Map<string, User>
  students: Array<Student>
  isLoading: boolean
  possibleSuggestion: number
  currentStudent: Student | null
}

const socket = new WebSocket(
  `ws://${
    process.env.NODE_ENV == 'development'
      ? '127.0.0.1:8000/'
      : 'sel2-5.ugent.be/'
  }ws/socket_server/`
)

export const useStudentStore = defineStore('user/student', {
  state: (): State => ({
    search: '',
    alumni: 'all',
    decision: 'none',
    byMe: false,
    onProject: false,
    skills: [],
    coaches: new Map(),
    students: [],
    isLoading: false,
    possibleSuggestion: -1,
    currentStudent: null,
  }),
  actions: {
    transformStudents(data: Student[]): void {
      for (const student of data) {
        if (student.finalDecision) {
          student.finalDecision.suggestion = parseInt(
            student.finalDecision.suggestion as unknown as string
          )
        }

        for (const suggestion of student.suggestions) {
          suggestion.suggestion = parseInt(
            suggestion.suggestion as unknown as string
          )
        }
      }
    },
    async loadStudents() {
      this.isLoading = true
      const filters = []

      if (this.search) filters.push(`search=${this.search}`)
      if (this.alumni === 'alumni') filters.push('alumni=true')
      if (this.decision !== 'none') filters.push(`suggestion=${this.decision}`)
      if (this.byMe === true) filters.push('suggested_by_user')
      if (this.onProject === true) filters.push('on_project')

      for (const skill of this.skills) {
        filters.push(`skills=${skill.id}`)
      }

      let url = ''
      if (filters) url = `?${filters.join('&')}`

      await instance.get<Student[]>(`students/${url}`).then(({ data }) => {
        this.transformStudents(data)

        this.students = data.map((student) => new Student(student))
      })

      this.isLoading = false
    },
    async loadStudent(studentId: number) {
      this.isLoading = true

      await instance.get(`students/${studentId}/`).then(async ({ data }) => {
        for (const suggestion of data.suggestions) {
          suggestion.suggestion = parseInt(suggestion.suggestion)
        }

        if (data.finalDecision) {
          data.finalDecision.suggestion = parseInt(
            data.finalDecision.suggestion
          )
        }

        const skills = [] as Skill[]

        for (let i = 0; i < data.skills.length; i++) {
          await instance.get(data.skills[i]).then(({ data }) => {
            skills.push(data)
          })
        }

        data.skills = skills
        this.currentStudent = new Student(data as Student)
      })

      this.isLoading = false
    },
    async updateSuggestion(
      studentId: number,
      coachId: number,
      suggestion: string,
      reason: string
    ) {
      // check if -1 is selected to delete suggestion
      if (this.possibleSuggestion == -1) {
        await instance.delete(`students/${studentId}/remove_suggestion/`)
      } else {
        await instance.post(`students/${studentId}/make_suggestion/`, {
          suggestion: this.possibleSuggestion,
          reason: reason,
        })
      }
      console.log('Coachid: ' + coachId)
      socket.send(
        JSON.stringify({
          studentId,
          coachId,
          suggestion,
          reason,
        })
      )

      await this.loadStudent(studentId)
    },
    async updateFinalDecision(
      studentId: number,
      possibleFinalDecision: string
    ) {
      let reason = ''

      if (
        this.currentStudent?.finalDecision?.suggestion.toString() ==
        possibleFinalDecision
      ) {
        reason = this.currentStudent.finalDecision.reason
      }

      // check if -1 is selected to delete decision
      if (possibleFinalDecision == '-1') {
        await instance.delete(`students/${studentId}/remove_final_decision/`)
      } else {
        await instance.post(`students/${studentId}/make_final_decision/`, {
          suggestion: possibleFinalDecision,
          reason: reason,
        })
      }

      await this.loadStudent(studentId)
    },
    receiveSuggestion({
      studentId,
      coachId,
      suggestion,
      reason,
    }: {
      studentId: number
      coachId: number
      suggestion: number
      reason: string
    }) {
      let ctr = 0

      // this.students id's start at 1
      while (ctr <= this.students.length && this.students[ctr].id !== studentId)
        ctr++

      // We found the corresponding student
      if (this.students[ctr].id === studentId) {
        const student = this.students[ctr]
        ctr = 0

        while (
          ctr < student.suggestions.length &&
          student.suggestions[ctr].coach.charAt(
            student.suggestions[ctr].coach.length - 2
          ) !== coachId.toString()
        )
          ctr++

        console.log(student.suggestions)
        if (ctr < student.suggestions.length) {
          // Update suggestion
          student.suggestions[ctr].suggestion = suggestion
          student.suggestions[ctr].reason = reason

          console.log('UPDATE')
        } else {
          console.log('NEW')
          // New suggestion
          const coaches = useCoachStore()
          const coach = coaches.users.filter(({ id }) => id === coachId)[0]
          student.suggestions.push({
            student: studentId,
            coachId: coachId,
            suggestion,
            reason,
            coach: coach.firstName,
            coachName: coach.firstName,
          })
        }
      }
    },
  },
})
