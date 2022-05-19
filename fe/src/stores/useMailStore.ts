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
    mailStudents: Array<Student>
    statusFilter: Array<number>
    mails: Map<number, Mail[]>
}

export const useMailStore = defineStore('user/mail', {
    state: (): State => ({
        isLoading: false,
        mailStudents: [],
        statusFilter: [],
        mails: new Map(),
    }),
    actions: {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        async loadStudentsMails(filters: any, setNumberOfRows: any) {
            this.isLoading = true
            const studentStore = useStudentStore()

            const {data} = await instance
                .get<{ results: Student[], count: number }>(`students/`,
                    {params: filters},
                )

            setNumberOfRows(data.count)

            for (const student of data.results) {
                await studentStore.transformStudent(student)
            }

            this.mailStudents = data.results.map((student) => new Student(student))

            this.isLoading = false
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
                .get(`emails/`, {params: params})
                .then(async ({ data }) => {
                    for (const mail of data.results) {
                        mail.time = new Date(mail.time).toLocaleString()
                        mail.type = parseInt(mail.type)

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
                        data.results.map((mail: Mail) => new Mail(mail))
                    )
                })

            this.isLoading = false
        },
        async updateStatus(student: Student) {
            await instance.patch(`students/${student.id}/`, {
                status: student.status,
            })
        },
        async sendMail(student: Student, type: number|null, date: string, info: string) {
            const authenticationStore = useAuthenticationStore()

            if (authenticationStore.loggedInUser) {
                await instance.post(`emails/`, {
                    sender: authenticationStore.loggedInUser.url,
                    receiver: student.url,
                    type: type,
                    time: date,
                    info: info,
                })
            }
        },
        async deleteMail(mail: Mail) {
            await instance.delete(`/emails/${mail.id}`)
        },
        /**
         * Get a csv of all mails in database
         */
        async csv(): Promise<{data: string, headers: object}> {
            return await instance.get('emails/export_csv')
        }
    }
})