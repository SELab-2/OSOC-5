import {defineStore} from "pinia";
import {instance} from "../utils/axios";
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";

export const useStudentStore = defineStore('user/student', {
  state: () => ({
    students: [],
    isLoadingStudents: false,
  }),
  actions: {
    async loadStudents() {
      this.isLoadingUsers = true
      await instance
        .get('students/')
        .then(({data}) => {
          this.isLoadingUsers = false
          this.students = convertObjectKeysToCamelCase(data)

          this.students.forEach((student, i) => {
            student.suggestions.forEach((suggestion, j) => {
              const pieces = suggestion.coach.split('/')

              suggestion.suggestion = parseInt(suggestion.suggestion)

              instance
                .get(`coaches/${pieces.slice(-2)[0]}/`)
                .then(({coach}) => {
                  console.log(coach)
                  Object.assign(this.students[i].suggestions[j], coach)
                })
            })
          })
        })
    },
    async updateSuggestion(studentId, suggestion) {
      await instance
        .post(`students/${studentId}/make_suggestion/`, {
          suggestion: suggestion,
          reason: ""
        }, {withCredentials: true})
        .then(({data}) => {
          console.log(data)
        })
    },
  }
})