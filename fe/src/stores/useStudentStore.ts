import {defineStore} from "pinia";
import {instance} from "../utils/axios";
import {convertObjectKeysToCamelCase} from "../utils/case-conversion";
import { User } from '../models/User'
import {Student} from "../models/Student";
import {Skill} from "../models/Skill";

interface State {
    search: string
    alumni: string
    decision: string
    byMe: boolean
    onProject: boolean
    skills: Array<Skill>
    skillsStudents: Map<string, Skill>
    coaches: Map<string, User>
    students: Array<Student>
    isLoading: boolean
    possibleSuggestion: number
    currentStudent: Student | null
}

export const useStudentStore = defineStore('user/student', {
    state: (): State => ({
        search: "",
        alumni: "all",
        decision: "none",
        byMe: false,
        onProject: false,
        skills: [],
        skillsStudents: new Map(),
        coaches: new Map(),
        students: [],
        isLoading: false,
        possibleSuggestion: -1,
        currentStudent: null,
    }),
    actions: {
        async transformStudent(student: any): Promise<void> {
            const skills = [] as Skill[]

            for (let i = 0; i < student.skills.length; i++) {
                if (this.skillsStudents.get(student.skills[i])) {
                    const skill = this.skillsStudents.get(student.skills[i].toString()) as Skill
                    skills.push(skill)
                } else {
                    await instance
                        .get(student.skills[i])
                        .then(({data}) => {
                            this.skillsStudents.set(student.skills[i].toString(), data)
                            skills.push(data)
                        })
                }
            }

            student.skills = skills

            if (student.finalDecision) {
                student.finalDecision.suggestion = parseInt(student.finalDecision.suggestion)
            }

            for (const suggestion of student.suggestions) {
                suggestion.suggestion = parseInt(suggestion.suggestion)
            }

            student.gender = parseInt(student.gender)
            student.language = parseInt(student.language)
            student.englishRating = parseInt(student.englishRating)
        },
        async loadStudents() {
            this.isLoading = true
            const filters = []

            if (this.search) filters.push(`search=${this.search}`)
            if (this.alumni === "alumni") filters.push("alum=true")
            if (this.alumni === "student coaches") filters.push("student_coach=true")
            if (this.decision !== "none") filters.push(`suggestion=${this.decision}`)
            if (this.byMe === true) filters.push("suggested_by_user")
            if (this.onProject === true) filters.push("on_project")

            for (const skill of this.skills) {
                filters.push(`skills=${skill.id}`)
            }

            let url = ""
            if (filters) url = `?${filters.join('&')}`

            await instance
                .get<Student[]>(`students/${url}`)
                .then(async ({data}) => {
                    for (const student of data) {
                        await this.transformStudent(student)
                    }

                    this.students = data.map((student) => new Student(student))
                })

            this.isLoading = false
        },
        async loadStudent(studentId: number) {
            this.isLoading = true

            await instance
                .get(`students/${studentId}/`)
                .then(async ({data}) => {
                    await this.transformStudent(data)

                    this.currentStudent = new Student(data as Student)
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
        async updateFinalDecision(studentId: number, possibleFinalDecision: string) {
            let reason = ""

            if (this.currentStudent?.finalDecision?.suggestion.toString() == possibleFinalDecision) {
                reason = this.currentStudent.finalDecision.reason
            }

            // check if -1 is selected to delete decision
            if (possibleFinalDecision == "-1") {
                await instance
                    .delete(`students/${studentId}/remove_final_decision/`)
            } else {
                await instance
                    .post(`students/${studentId}/make_final_decision/`, {
                        suggestion: possibleFinalDecision,
                        reason: reason
                    })
            }

            await this.loadStudent(studentId)
        }
    }
})