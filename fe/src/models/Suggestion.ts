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

  constructor(obj: SuggestionInterface)
  constructor(
    student: number,
    coach: { id: number; firstName: string; lastName: string; url: string },
    suggestion: number,
    reason: string
  )

  constructor(...args: any[]){
    if (args.length == 1) {
      Object.assign(this, args[0])
    } else {
      this.student = args[0]
      this.coach = args[1]
      this.suggestion = args[2]
      this.reason = args[3]
    }
  }
}
