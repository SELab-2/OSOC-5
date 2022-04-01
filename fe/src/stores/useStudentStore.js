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
      let url = ""
      const urlCoaches = new Set()

      await instance
        .get('students/')
        .then(({data}) => {
          this.isLoadingUsers = false
          this.students = convertObjectKeysToCamelCase(data)
        })

      const coaches = new Map()

      for (let i = 0; i < this.students.length; i++) {
        for (let j = 0; j < this.students[i].suggestions.length; j++) {
          this.students[i].suggestions[j].suggestion = parseInt(this.students[i].suggestions[j].suggestion)

          let coach_url = this.students[i].suggestions[j].coach

          if (! coaches.has(coach_url)) {
            await instance
              .get(coach_url)
              .then(({data}) => {
                Object.assign(this.students[i].suggestions[j], data)
                coaches.set(coach_url, data)
              })
          } else {
            Object.assign(this.students[i].suggestions[j], coaches.get(coach_url))
          }

        }
      }
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