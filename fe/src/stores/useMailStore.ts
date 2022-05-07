import {Student} from "../models/Student";
import {Mail} from "../models/Mail";
import {defineStore} from "pinia";
import {instance} from "../utils/axios";
import {User} from "../models/User";
import {useStudentStore} from "./useStudentStore";
import {useAuthenticationStore} from "./useAuthenticationStore";

interface State {
    isLoading: boolean
    searchMails: string
    mailStudents: Array<Student>
    mails: Map<number, Mail[]>
    selectedStudents: Array<Student>
}

export const useMailStore = defineStore('user/mail', {
    state: (): State => ({
        isLoading: false,
        searchMails: '',
        mailStudents: [],
        mails: new Map(),
        selectedStudents: []
    }),
    actions: {
        async loadStudentsMails() {
            this.isLoading = true
            const studentStore = useStudentStore()

            const filters = []
            if (this.searchMails) filters.push(`search=${this.searchMails}`)

            let url = ''
            if (filters) url = `?${filters.join('&')}`

            await instance
                .get<{ results: Student[] }>(`students/${url}`)
                .then(async ({ data }) => {
                    for (const student of data.results) {
                        await studentStore.transformStudent(student)
                    }

                    this.mailStudents = data.results.map((student) => new Student(student))
                })

            this.isLoading = false
        },
        async getMails(student: Student) {
            this.isLoading = true

            const studentStore = useStudentStore()

            await instance
                .get<{ results: Mail[] }>(`emails/?receiver=${student.id}`)
                .then(async ({ data }) => {
                    for (const mail of data.results) {
                        mail.time = new Date(mail.time).toLocaleString()

                        const sender = mail.sender

                        if (typeof sender === 'string') {
                            if (studentStore.coaches.has(sender)) {
                                mail.sender = studentStore.coaches.get(sender)!
                            } else {
                                await instance.get<User>(sender).then(({ data }) => {
                                    const coach = new User(data)
                                    mail.sender = coach
                                    studentStore.coaches.set(sender, coach)
                                })
                            }
                        }
                    }

                    this.mails.set(
                        student.id,
                        data.results.map((mail) => new Mail(mail))
                    )
                })

            this.isLoading = true
        },
        async updateStatus(student: Student) {
            await instance.patch(`students/${student.id}/`, {
                status: student.status,
            })
        },
        async sendMail(student: Student, date: string, info: string) {
            const authenticationStore = useAuthenticationStore()

            if (authenticationStore.loggedInUser) {
                await instance.post(`emails/`, {
                    sender: authenticationStore.loggedInUser.url,
                    receiver: student.url,
                    time: date,
                    info: info,
                })
            }
        },
        async deleteMail(mail: Mail) {
            await instance.delete(`/emails/${mail.id}`)
        },
    }
})