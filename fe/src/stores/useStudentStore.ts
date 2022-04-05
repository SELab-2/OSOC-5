import {defineStore} from "pinia";
import {instance} from "../utils/axios";
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";
import { User } from '../models/User'
import {Student} from "../models/Student";
import {Suggestion} from "../models/Suggestion";

interface State {
    coaches: Map<string, User>
    students: Array<Student>
    isLoading: boolean
    currentStudent: Student | null
}

export const useStudentStore = defineStore('user/student', {
    state: (): State => ({
        coaches: new Map(),
        students: [],
        isLoading: false,
        currentStudent: null,
    }),
    actions: {
        async loadStudents() {
            this.isLoading = true

            await instance
                .get('students/')
                .then(({data}) => {
                    this.isLoading = false

                    for (const student of data) {
                        for (const suggestion of student.suggestions) {
                            suggestion.suggestion = parseInt(suggestion.suggestion)
                        }
                    }

                    this.students = convertObjectKeysToCamelCase(data) as never as Student[]
                })

            for (const student of this.students) {
                for (const suggestion of student.suggestions) {

                    const coachUrl = suggestion.coach

                    if (! this.coaches.has(coachUrl)) {
                        await instance
                            .get(coachUrl)
                            .then(({data}) => {
                                Object.assign(suggestion, data)
                                this.coaches.set(coachUrl, data)
                            })
                    } else {
                        Object.assign(suggestion, this.coaches.get(coachUrl))
                    }

                }
            }
        },
        async loadStudent(studentId: number) {
            this.isLoading = true

            await instance
                .get(`students/${studentId}/`)
                .then(({data}) => {
                    for (const suggestion of data.suggestions) {
                        suggestion.suggestion = parseInt(suggestion.suggestion)
                    }

                    this.currentStudent = convertObjectKeysToCamelCase(data) as never as Student
                })

            if (this.currentStudent !== null) {
                for (let i = 0; i < this.currentStudent.suggestions.length; i++) {
                    const coachUrl = this.currentStudent.suggestions[i].coach

                    await instance
                        .get(coachUrl)
                        .then(({data}) => {
                            if (this.currentStudent !== null) {
                                Object.assign(this.currentStudent.suggestions[i], data)
                            }
                        })
                }

                this.isLoading = false
            }
        },
        async updateSuggestion(studentId: number, suggestion: number, reason: string) {
            await instance
                .post(`students/${studentId}/make_suggestion/`, {
                    suggestion: suggestion,
                    reason: reason
                })

            await this.loadStudent(studentId)
        },
    }
})