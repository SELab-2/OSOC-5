interface Suggestion {
  student: number,
  coach: number,
  suggestion: SuggestionChoice,
  reason: string
}

enum SuggestionChoice {
  Yes = 0,
  No = 1,
  Maybe = 2
}