export interface SuggestionInterface {
  student: number
  coach: number
  suggestion: SuggestionChoice
  reason: string
}

enum SuggestionChoice {
  Yes = 0,
  No = 1,
  Maybe = 2,
}

export class Suggestion implements SuggestionInterface {
  student: number
  coach: number
  suggestion: SuggestionChoice
  reason: string

  constructor(
    student: number,
    coach: number,
    suggestion: SuggestionChoice,
    reason: string
  ) {
    this.student = student
    this.coach = coach
    this.suggestion = suggestion
    this.reason = reason
  }
}
