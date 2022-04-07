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
    possibleSuggestion: number
    possibleFinalDecision: number
    currentStudent: Student | null
}

export const useStudentStore = defineStore('user/student', {
    state: (): State => ({
        coaches: new Map(),
        students: [],
        isLoading: false,
        possibleSuggestion: -1,
        possibleFinalDecision: -1,
        currentStudent: null,
    }),
    actions: {
        async loadStudents(): Promise<void> {
            this.isLoading = true

            await instance
                .get('students/')
                .then(({data}) => {
                    for (const student of data) {
                        if (student.final_decision) {
                            student.final_decision.suggestion = parseInt(student.final_decision.suggestion)
                        }

                        for (const suggestion of student.suggestions) {
                            suggestion.suggestion = parseInt(suggestion.suggestion)
                        }
                    }

                    this.students = convertObjectKeysToCamelCase(data) as never as Student[]
                })

            this.isLoading = false
        },
        async loadStudent(studentId: number) {
            this.isLoading = true

            await instance
                .get(`students/${studentId}/`)
                .then(({data}) => {
                    for (const suggestion of data.suggestions) {
                        suggestion.suggestion = parseInt(suggestion.suggestion)
                    }

                    if (data.final_decision) {
                        data.final_decision.suggestion = parseInt(data.final_decision.suggestion)
                    }

                    this.currentStudent = convertObjectKeysToCamelCase(data) as never as Student
                    this.possibleFinalDecision = this.currentStudent.finalDecision?.suggestion || -1
                })

            this.isLoading = false
        },
        async updateSuggestion(studentId: number, reason: string) {
            // check if -1 is selected to delete suggestion
            if (this.possibleSuggestion == -1) {
                await instance
                    .delete(`students/${studentId}/remove_suggestion/`)
            } else {
                await instance
                    .post(`students/${studentId}/make_suggestion/`, {
                        suggestion: this.possibleSuggestion,
                        reason: reason
                    })
            }

            await this.loadStudent(studentId)
        },
        async updateFinalDecision(studentId: number) {
            console.log(this.possibleFinalDecision)
            // check if -1 is selected to delete decision
            if (this.possibleFinalDecision == null) {
                await instance
                    .delete(`students/${studentId}/remove_final_decision/`)
            } else {
                await instance
                    .post(`students/${studentId}/make_final_decision/`, {
                        suggestion: this.possibleFinalDecision,
                        reason: ""
                    })
            }

            await this.loadStudent(studentId)
        }
    }
})