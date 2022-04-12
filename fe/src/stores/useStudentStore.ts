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
        transformStudents(data: any): void {
            for (const student of data) {
                if (student.finalDecision) {
                    student.finalDecision.suggestion = parseInt(student.finalDecision.suggestion)
                }

                for (const suggestion of student.suggestions) {
                    suggestion.suggestion = parseInt(suggestion.suggestion)
                }
            }
        },
        async loadStudents() {
            this.isLoading = true
            const filters = []

            if (this.search) filters.push(`search=${this.search}`)
            if (this.alumni === "alumni") filters.push("alumni=true")
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
                        const skills = [] as Skill[]

                        for (let i = 0; i < student.skills.length; i++) {
                            if (this.skillsStudents.get(student.skills[i].toString())) {
                                const skill = this.skillsStudents.get(student.skills[i].toString()) as Skill
                                skills.push(skill)
                            } else {
                                await instance
                                    .get(student.skills[i].toString())
                                    .then(({data}) => {
                                        this.skillsStudents.set(student.skills[i].toString(), data)
                                        skills.push(data)
                                    })
                            }
                        }

                        student.skills = skills
                    }
                    console.log(data)

                    this.transformStudents(data)

                    this.students = data.map((student) => new Student(student))
                })



            // for (let i = 0; i < data.skills.length; i++) {
            //     await instance
            //         .get(data.skills[i])
            //         .then(({data}) => {
            //             skills.push(data)
            //         })
            // }
            //
            // data.skills = skills

            this.isLoading = false
        },
        async loadStudent(studentId: number) {
            this.isLoading = true

            await instance
                .get(`students/${studentId}/`)
                .then(async ({data}) => {
                    console.log(data)
                    for (const suggestion of data.suggestions) {
                        suggestion.suggestion = parseInt(suggestion.suggestion)
                    }

                    if (data.finalDecision) {
                        data.finalDecision.suggestion = parseInt(data.finalDecision.suggestion)
                    }

                    const skills = [] as Skill[]

                    for (let i = 0; i < data.skills.length; i++) {
                        await instance
                            .get(data.skills[i])
                            .then(({data}) => {
                                skills.push(data)
                            })
                    }

                    data.skills = skills
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