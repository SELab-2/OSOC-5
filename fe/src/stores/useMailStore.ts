import {Student} from "../models/Student";
import {Mail} from "../models/Mail";
import {defineStore} from "pinia";
import qs from "qs";
import {instance} from "../utils/axios";
import {User} from "../models/User";
import {useStudentStore} from "./useStudentStore";
import {useAuthenticationStore} from "./useAuthenticationStore";

interface State {
    isLoading: boolean
    searchMails: string
    mailStudents: Array<Student>
    statusFilter: Array<number>
    mails: Map<number, Mail[]>
}

export const useMailStore = defineStore('user/mail', {
    state: (): State => ({
        isLoading: false,
        searchMails: '',
        mailStudents: [],
        statusFilter: [],
        mails: new Map(),
    }),
    actions: {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        async loadStudentsMails(pagination: any, setNumberOfRows: any) {
            this.isLoading = true
            const studentStore = useStudentStore()

            const params = {
                page_size: pagination.rowsPerPage,
                page: pagination.page
            } as {page_size: number, page: number, search: string, ordering: string, status: number[]}

            if (this.searchMails) params.search = this.searchMails
            const order = pagination.descending ? '-' : '+'
            if (pagination.sortBy === 'name') {
                params.ordering = `${order}first_name,${order}last_name`
            } else if (pagination.sortBy !== null) {
                params.ordering = `${order}${pagination.sortBy}`
            }
            if (this.statusFilter.length > 0) params.status = this.statusFilter

            await instance
                .get<{ results: Student[], count: number }>(`students/`, {
                    params: params,
                    paramsSerializer: params => {
                        return qs.stringify(params, {arrayFormat: "repeat"})
                    }
                })
                .then(async ({ data }) => {
                    setNumberOfRows(data.count)

                    for (const student of data.results) {
                        await studentStore.transformStudent(student)
                    }

                    this.mailStudents = data.results.map((student) => new Student(student))

                    this.isLoading = false
                })
        },
        async updateStatusStudents(updateValue: number, students: Array<Student>) {
          if (students.length > 0) {
              await instance.post('students/bulk_status/', {
                  status: updateValue,
                  students: students.map(student => student.url)
              })
          }
        },
        async getMails(student: Student) {
            this.isLoading = true

            const studentStore = useStudentStore()

            const params = {
                receiver: student.id
            }

            await instance
                .get<{ results: Mail[] }>(`emails/`, {params: params})
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