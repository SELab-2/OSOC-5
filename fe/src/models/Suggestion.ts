export interface SuggestionInterface {
  email: string | null  // must be deleted later
  student: number
  coach: string
  suggestion: number
  reason: string
}

export class Suggestion implements SuggestionInterface {
  student: number
  coach: number
  suggestion: number
  reason: string

  constructor(
    student: number,
    coach: number,
    suggestion: number,
    reason: string
  ) {
    this.student = student
    this.coach = coach
    this.suggestion = suggestion
    this.reason = reason
  }
}
