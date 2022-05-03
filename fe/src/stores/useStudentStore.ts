import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { User } from '../models/User'
import { Student, StudentInterface } from '../models/Student'
import { Skill } from '../models/Skill'
import { Mail } from '../models/Mail'
import { useAuthenticationStore } from './useAuthenticationStore'
import { useCoachStore } from './useCoachStore'

interface State {
  search: string
  searchMails: string
  status: string
  alumni: string
  decision: string
  byMe: string
  onProject: string
  skills: Array<Skill>
  skillsStudents: Map<string, Skill>
  coaches: Map<string, User>
  students: Array<Student>
  mailStudents: Array<Student>
  mails: Map<number, Mail[]>
  isLoading: boolean
  possibleSuggestion: number
  currentStudent: Student | null
  nextPage: string | null
}

export const useStudentStore = defineStore('user/student', {
  state: (): State => ({
    search: '',
    searchMails: '',
    status: '',
    alumni: 'all',
    decision: 'none',
    byMe: 'maybe',
    onProject: 'maybe',
    skills: [],
    skillsStudents: new Map(),
    coaches: new Map(),
    students: [],
    mailStudents: [],
    mails: new Map(),
    isLoading: false,
    possibleSuggestion: -1,
    currentStudent: null,
    nextPage: ''
  }),
  actions: {
    async getStudent(url: string): Promise<Student> {
      const student = this.students.find((student) => student.url === url)
      if (student) return student
      const { data } = await instance.get<StudentInterface>(url)
      await this.transformStudent(data)

      // Check again if not present, it could be added in the meantime.
      const student2 = this.students.find((student) => student.url === url)
      if (student2) return student2

      const newstudent = new Student(data)
      this.students.push(newstudent)
      return newstudent
    },
    async transformStudent(student: any): Promise<void> {
      const skills = [] as Skill[]

      for (let i = 0; i < student.skills.length; i++) {
        if (this.skillsStudents.get(student.skills[i])) {
          const skill = this.skillsStudents.get(
            student.skills[i].toString()
          ) as Skill
          skills.push(skill)
        } else {
          await instance.get(student.skills[i]).then(({ data }) => {
            this.skillsStudents.set(student.skills[i].toString(), data)
            skills.push(data)
          })
        }
      }

      student.skills = skills

      if (student.finalDecision) {
        student.finalDecision.suggestion = parseInt(
          student.finalDecision.suggestion
        )
      }

      for (const suggestion of student.suggestions) {
        suggestion.suggestion = parseInt(suggestion.suggestion)
      }

      student.gender = parseInt(student.gender)
      student.language = parseInt(student.language)
      student.englishRating = parseInt(student.englishRating)
    },
    async loadStudents() {
      console.log('in there')
      this.isLoading = true
      const filters = []

      if (this.search) filters.push(`search=${this.search}`)
      if (this.alumni === 'alumni') filters.push('alum=true')
      if (this.alumni === 'student coaches') filters.push('student_coach=true')
      if (this.decision !== 'none') filters.push(`suggestion=${this.decision}`)
      if (this.byMe !== 'maybe') filters.push(`suggested_by_user=${this.byMe}`)
      if (this.onProject !== 'maybe') filters.push(`on_project=${this.onProject}`)
      if (this.status) filters.push(`status=${this.status}`)

      for (const skill of this.skills) {
        filters.push(`skills=${skill.id}`)
      }

      let url = ''
      if (filters.length > 0) {
        url = `&${filters.join('&')}`
      }

      await instance
        .get(`students/?page=1${url}`)
        .then(async ({ data }) => {
          this.nextPage = data.next

          for (const student of data.results) {
            await this.transformStudent(student)
          }

          this.students = data.results.map((student: Student) => new Student(student))
        })

      this.isLoading = false
    },
    async loadNext(index: number, done: any) {
      if (this.nextPage === null) {
        done(true)
        return
      }

      if (this.nextPage !== '') {
        await instance
            .get(this.nextPage)
            .then(async ({data}) => {
              this.nextPage = data.next

              for (const student of data.results) {
                await this.transformStudent(student)
              }

              this.students.push(...data.results.map((student: Student) => new Student(student)))
            })
      }
      done()
    },
    async loadStudentsMails() {
      this.isLoading = true
      const filters = []

      if (this.search) filters.push(`search=${this.searchMails}`)

      let url = ''
      if (filters) url = `?${filters.join('&')}`

      await instance
        .get<Student[]>(`students/${url}`)
        .then(async ({ data }) => {
          for (const student of data) {
            await this.transformStudent(student)
          }

          this.mailStudents = data.map((student) => new Student(student))
        })

      this.isLoading = false
    },
    async loadStudent(studentId: number) {
      this.isLoading = true

      await instance.get(`students/${studentId}/`).then(async ({ data }) => {
        await this.transformStudent(data)

        this.currentStudent = new Student(data as Student)
      })

      this.isLoading = false
    },
    async updateSuggestion(studentId: number, reason: string) {
      // check if -1 is selected to delete suggestion
      if (this.possibleSuggestion == -1) {
        await instance.delete(`students/${studentId}/remove_suggestion/`)
      } else {
        await instance.post(`students/${studentId}/make_suggestion/`, {
          suggestion: this.possibleSuggestion,
          reason: reason,
        })
      }

      await this.loadStudent(studentId)
    },
    async updateFinalDecision(
      studentId: number,
      possibleFinalDecision: string
    ) {
      let reason = ''

      if (
        this.currentStudent?.finalDecision?.suggestion.toString() ==
        possibleFinalDecision
      ) {
        reason = this.currentStudent.finalDecision.reason
      }

      // check if -1 is selected to delete decision
      if (possibleFinalDecision == '-1') {
        await instance.delete(`students/${studentId}/remove_final_decision/`)
      } else {
        await instance.post(`students/${studentId}/make_final_decision/`, {
          suggestion: possibleFinalDecision,
          reason: reason,
        })
      }

      await this.loadStudent(studentId)
    },
    async updateStatus(student: Student) {
      await instance.patch(`students/${student.id}/`, {
        status: student.status,
      })
    },
    async getMails(student: Student) {
      this.isLoading = true

      await instance
        .get<Mail[]>(`emails/?receiver=${student.id}`)
        .then(async ({ data }) => {
          for (const mail of data) {
            mail.time = new Date(mail.time).toLocaleString()

            const sender = mail.sender

            if (typeof sender === 'string') {
              if (this.coaches.has(sender)) {
                mail.sender = this.coaches.get(sender)!
              } else {
                await instance.get<User>(sender).then(({ data }) => {
                  const coach = new User(data)
                  mail.sender = coach
                  this.coaches.set(sender, coach)
                })
              }
            }
          }

          this.mails.set(
            student.id,
            data.map((mail) => new Mail(mail))
          )
        })

      this.isLoading = true
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
    async receiveSuggestion({
      student_id,
      coach,
      suggestion,
      reason,
    }: {
      student_id: number
      coach: { id: number; firstName: string; lastName: string; url: string }
      suggestion: string
      reason: string
    }) {
      const studentId = Number(student_id)
      const coachId = coach.id
      const suggestionParsed = Number.parseInt(suggestion)

      const student = this.students.filter(({ id }) => id === studentId)[0]

      // We found the corresponding student
      if (student) {
        let ctr = 0
        while (
          ctr < student.suggestions.length &&
          student.suggestions[ctr].coach.id !== coachId
        )
          ctr++

        if (ctr < student.suggestions.length) {
          // Update suggestion
          student.suggestions[ctr].suggestion = suggestionParsed
          student.suggestions[ctr].reason = reason
        } else {
          // New suggestion
          const coaches = useCoachStore()
          const coach = await coaches.getUser(`/coaches/${coachId.toString()}`)

          student.suggestions.push({
            student: studentId,
            suggestion: suggestionParsed,
            reason,
            coach,
          })
        }

        if (this.currentStudent?.id === studentId) this.currentStudent = student
      }
    },
    removeSuggestion({
      student,
      coach,
    }: {
      student: string
      coach: { id: number }
    }) {
      const studentId = Number.parseInt(student)
      const coachId = coach.id

      const matchingStudent = this.students.filter(
        ({ id }) => id === studentId
      )[0]

      // We found the corresponding student
      if (matchingStudent) {
        const suggestion = matchingStudent.suggestions.findIndex(
          (s) => s.coach.id === coachId
        )

        // Corresponding suggestion is found
        if (suggestion !== -1) matchingStudent.suggestions.splice(suggestion, 1)

        if (this.currentStudent?.id === studentId)
          this.currentStudent = matchingStudent
      }
    },
    receiveFinalDecision({
      student_id,
      suggestion,
      coach,
      reason,
    }: {
      student_id: string
      coach_id: string
      suggestion: number
      coach: { id: number; firstName: string; lastName: string; url: string }
      reason: string
    }) {
      const studentId = Number.parseInt(student_id)

      const student = this.students.filter(({ id }) => id === studentId)[0]

      // We found the corresponding student
      if (student) {
        const finalDecision = {
          student: studentId,
          coach: coach,
          suggestion,
          reason,
        }
        student.finalDecision = finalDecision

        if (this.currentStudent?.id === studentId) this.currentStudent = student
      }
    },
    removeFinalDecision({ student_id }: { student_id: string }) {
      const studentId = Number.parseInt(student_id)

      const student = this.students.filter(({ id }) => id === studentId)[0]

      // We found the corresponding student
      if (student) {
        student.finalDecision = null

        if (this.currentStudent?.id === studentId) this.currentStudent = student
      }
    },
  },
})
