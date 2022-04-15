export interface SuggestionInterface {
  student: number
  coach: string
  coachId: number
  coachName: string
  suggestion: number
  reason: string
}

export class Suggestion implements SuggestionInterface {
  student: number
  coach: string
  suggestion: number
  coachId: number
  coachName: string
  reason: string

  constructor(
    student: number,
    coach: string,
    suggestion: number,
    coachId: number,
    coachName: string,
    reason: string,
  ) {
    this.student = student
    this.coach = coach
    this.coachId = coachId
    this.coachName = coachName
    this.suggestion = suggestion
    this.reason = reason
  }
}
