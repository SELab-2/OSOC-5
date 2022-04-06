import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { User } from '../models/User'
import { Student } from '../models/Student'

interface State {
  coaches: Map<string, User>
  students: Array<Student>
  isLoading: boolean
  currentStudent: Student | null
}

const socket = new WebSocket(
  `ws://${
    process.env.NODE_ENV == 'development'
      ? 'http://127.0.0.1:8000/'
      : 'https://sel2-5.ugent.be/'
  }/ws/socket_server/`
)

export const useStudentStore = defineStore('user/student', {
  state: (): State => ({
    coaches: new Map(),
    students: [],
    isLoading: false,
    currentStudent: null,
  }),
  actions: {
    async loadStudents(): Promise<void> {
      this.isLoading = true

      const { data } = await instance.get('students/')
      this.isLoading = false

      for (const student of data) {
        for (const suggestion of student.suggestions) {
          suggestion.suggestion = parseInt(suggestion.suggestion)
        }
      }

      this.students = convertObjectKeysToCamelCase(data) as never as Student[]

      for (const student of this.students) {
        for (const suggestion of student.suggestions) {
          const coachUrl = suggestion.coach

          if (!this.coaches.has(coachUrl)) {
            const { data } = await instance.get(coachUrl)
            Object.assign(suggestion, data)
            this.coaches.set(coachUrl, data)
          } else {
            Object.assign(suggestion, this.coaches.get(coachUrl))
          }
        }
      }
    },
    async loadStudent(studentId: number) {
      this.isLoading = true

      await instance.get(`students/${studentId}/`).then(({ data }) => {
        for (const suggestion of data.suggestions) {
          suggestion.suggestion = parseInt(suggestion.suggestion)
        }

        this.currentStudent = convertObjectKeysToCamelCase(
          data
        ) as never as Student
      })

      if (this.currentStudent !== null) {
        for (let i = 0; i < this.currentStudent.suggestions.length; i++) {
          const coachUrl = this.currentStudent.suggestions[i].coach

          await instance.get(coachUrl).then(({ data }) => {
            if (this.currentStudent !== null) {
              Object.assign(this.currentStudent.suggestions[i], data)
            }
          })
        }

        this.isLoading = false
      }
    },
    async updateSuggestion(
      studentId: number,
      coachId: number,
      suggestion: number,
      reason: string
    ) {
      await instance.post(`students/${studentId}/make_suggestion/`, {
        suggestion: suggestion,
        reason: reason,
      })

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

      console.log(studentId)
      console.log(ctr)
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

        if (ctr < student.suggestions.length) {
          student.suggestions[ctr].suggestion = suggestion
          student.suggestions[ctr].reason = reason
        } else {
          student.suggestions.push({
            student: studentId,
            coach: '',
            suggestion,
            reason,
            email: null,
          })
        }
      }
    },
  },
})
