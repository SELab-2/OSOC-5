import { defineStore } from 'pinia'
import { instance } from '../utils/axios'
import { User } from '../models/User'
import { Student, StudentInterface } from '../models/Student'
import { Skill } from '../models/Skill'

interface State {
  search: string
  status: string
  alumni: string
  decision: string
  byMe: string
  onProject: string
  skills: Array<Skill>
  skillsStudents: Map<string, Skill>
  coaches: Map<string, User>
  students: Array<Student>
  isLoading: boolean
  possibleSuggestion: number
  currentStudent: Student | null
  nextPage: string | null
}

export const useStudentStore = defineStore('user/student', {
  state: (): State => ({
    search: '',
    status: '',
    alumni: 'all',
    decision: 'none',
    byMe: 'maybe',
    onProject: 'maybe',
    skills: [],
    skillsStudents: new Map(),
    coaches: new Map(),
    students: [],
    isLoading: false,
    possibleSuggestion: -1,
    currentStudent: null,
    nextPage: '',
  }),
  actions: {
    /**
     * Get info about a student using its url
     * @param url from which the student information can be retrieved
     */
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
    /**
     * Transform a student filling in its skills and transforming some strings to numbers
     * @param student to transform
     */
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
    /**
     * Load all students depending on chosen filters
     */
    async loadStudents() {
      this.isLoading = true
      const filters = []

      if (this.search) filters.push(`search=${this.search}`)
      if (this.alumni === 'alumni') filters.push('alum=true')
      if (this.alumni === 'student coaches') filters.push('student_coach=true')
      if (this.decision !== 'none') filters.push(`suggestion=${this.decision}`)
      if (this.byMe !== 'maybe') filters.push(`suggested_by_user=${this.byMe}`)
      if (this.onProject !== 'maybe')
        filters.push(`on_project=${this.onProject}`)
      if (this.status) filters.push(`status=${this.status}`)

      for (const skill of this.skills) {
        filters.push(`skills=${skill.id}`)
      }

      let url = ''
      if (filters.length > 0) {
        url = `&${filters.join('&')}`
      }

      await instance
        .get<{ results: Student[]; next: string }>(`students/?page=1${url}`)
        .then(async ({ data }) => {
          this.nextPage = data.next

          for (const student of data.results) {
            await this.transformStudent(student)
          }

          this.students = data.results.map((student) => new Student(student))
        })

      this.isLoading = false
    },
    /**
     * Load next x students and add them to the rest of the students
     * @param index current index in scroll
     * @param done to be called when done fetching new student
     */
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async loadNext(index: number, done: any) {
      this.isLoading = true

      if (this.nextPage == null) {
        done(true)
        this.isLoading = false
        return
      }

      if (this.nextPage !== '') {
        await instance.get(this.nextPage).then(async ({ data }) => {
          this.nextPage = data.next

          for (const student of data.results) {
            await this.transformStudent(student)
          }

          this.students.push(
            ...data.results.map((student: Student) => new Student(student))
          )
        })
      }
      done()
      this.isLoading = false
    },
    /**
     * Load a student by its id
     * @param studentId the id of the student
     */
    async loadStudent(studentId: number) {
      this.isLoading = true

      await instance.get(`students/${studentId}/`).then(async ({ data }) => {
        await this.transformStudent(data)

        this.currentStudent = new Student(data as Student)
      })

      this.isLoading = false
    },
    /**
     * Update your suggestion on a student
     * @param studentId the id of the student
     * @param reason the reason to do the suggestion
     */
    async updateSuggestion(studentId: number, reason: string) {
      // check if -1 is selected to delete suggestion
      if (this.possibleSuggestion === -1) {
        await instance.delete(`students/${studentId}/remove_suggestion/`)
      } else {
        await instance.post(`students/${studentId}/make_suggestion/`, {
          suggestion: this.possibleSuggestion,
          reason: reason,
        })
      }

      await this.loadStudent(studentId)
    },
    /**
     * Update the final decision on a student
     * @param studentId the id of the student
     * @param possibleFinalDecision the final decision to make on this student
     */
    async updateFinalDecision(
      studentId: number,
      possibleFinalDecision: number
    ) {
      let reason = ''

      // keep reason if reason is given in suggestion
      if (
        this.currentStudent?.finalDecision?.suggestion == possibleFinalDecision
      ) {
        reason = this.currentStudent.finalDecision.reason
      }

      // check if -1 is selected to delete decision
      if (possibleFinalDecision === -1) {
        await instance.delete(`students/${studentId}/remove_final_decision/`)
      } else {
        await instance.post(`students/${studentId}/make_final_decision/`, {
          suggestion: possibleFinalDecision,
          reason: reason,
        })
      }

      await this.loadStudent(studentId)
    },
    /**
     * Receive a suggestion that another user made on this student
     * @param student_id the id of the student
     * @param coach the coach that made the suggestion
     * @param suggestion the suggestion that was made
     * @param reason the reason why this suggestion was made
     */
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
    /**
     * Remove a suggestion of a coach on a student
     * @param student to remove the suggestion from
     * @param coach from who the suggestion is deleted
     */
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
    /**
     * Receive a final decision that another user made on this student
     * @param student_id the id of the student
     * @param coach the coach that made the suggestion
     * @param suggestion the suggestion that was made
     * @param reason the reason why this suggestion was made
     */
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
    /**
     * Remove a final decision of a coach on a student
     * @param student to remove the suggestion from
     * @param coach from who the suggestion is deleted
     */
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
