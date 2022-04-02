import {defineStore} from "pinia";
import {instance} from "../utils/axios";
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";

export const useStudentStore = defineStore('user/student', {
  state: () => ({
    coaches: new Map(),
    students: [],
    isLoading: false,
    currentStudent: null,
  }),
  actions: {
    async loadStudents() {
      this.isLoading = true
      let url = ""
      const urlCoaches = new Set()

      await instance
        .get('students/')
        .then(({data}) => {
          this.isLoading = false
          this.students = convertObjectKeysToCamelCase(data)
        })

      for (let student of this.students) {
        for (let j = 0; j < student.suggestions.length; j++) {
          student.suggestions[j].suggestion = parseInt(student.suggestions[j].suggestion)

          let coachUrl = student.suggestions[j].coach

          if (! this.coaches.has(coachUrl)) {
            await instance
              .get(coachUrl)
              .then(({data}) => {
                Object.assign(student.suggestions[j], data)
                this.coaches.set(coachUrl, data)
              })
          } else {
            Object.assign(student.suggestions[j], this.coaches.get(coachUrl))
          }

        }
      }
    },
    async loadStudent(studentId) {
      this.isLoading = true

      await instance
        .get(`students/${studentId}/`)
        .then(({data}) => {
          this.currentStudent = convertObjectKeysToCamelCase(data)
          for (let suggestion of this.currentStudent.suggestions) {
            suggestion.suggestion = parseInt(suggestion.suggestion)
          }
        })

      for (let i = 0; i < this.currentStudent.suggestions.length; i++) {
        let coachUrl = this.currentStudent.suggestions[i].coach

        await instance
          .get(coachUrl)
          .then(({data}) => {
            Object.assign(this.currentStudent.suggestions[i], data)
            console.log(this.currentStudent.suggestions[i])
          })
      }

      this.isLoading = false
    },
    async updateSuggestion(studentId, suggestion) {
      await instance
        .post(`students/${studentId}/make_suggestion/`, {
          suggestion: suggestion,
          reason: ""
        }).then(({data}) => {
          console.log(data)
        })
    },
  }
})