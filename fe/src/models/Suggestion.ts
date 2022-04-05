export interface SuggestionInterface {
  email: string | null  // must be deleted later
  student: number
  coach: string
  suggestion: number
  reason: string
}

export class Suggestion implements SuggestionInterface {
  student: number
  coach: string
  suggestion: number
  reason: string
  email: string | null

  constructor(
    student: number,
    coach: string,
    suggestion: number,
    reason: string,
    email: string | null
  ) {
    this.student = student
    this.coach = coach
    this.suggestion = suggestion
    this.reason = reason
    this.email = email
  }
}
