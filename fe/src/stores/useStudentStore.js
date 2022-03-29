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
      instance
        .get('students/')
        .then(({data}) => {
          this.isLoadingUsers = false
          this.students = convertObjectKeysToCamelCase(data).results

          this.students.forEach((student, i) => {
            student.suggestions.forEach((suggestion, j) => {
              const pieces = suggestion.coach.split('/')
              const url = 'coaches/' + pieces.slice(-2)[0] + '/'

              suggestion.suggestion = parseInt(suggestion.suggestion)

              instance
                .get(url)
                .then(({data}) => {
                  Object.assign(this.students[i].suggestions[j], data)
                })
            })
          })
        })
    }
  }
})