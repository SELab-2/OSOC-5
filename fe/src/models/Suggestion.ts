export interface SuggestionInterface {
  student: number
  coach: { id: number; firstName: string; lastName: string; url: string }
  suggestion: number
  reason: string
}

export class Suggestion implements SuggestionInterface {
  student: number
  coach: { id: number; firstName: string; lastName: string; url: string }
  suggestion: number
  reason: string

  constructor(
    student: number,
    coach: { id: number; firstName: string; lastName: string; url: string },
    suggestion: number,
    reason: string
  ) {
    this.student = student
    this.coach = coach
    this.suggestion = suggestion
    this.reason = reason
  }
}
