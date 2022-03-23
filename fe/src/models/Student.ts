interface Student {
  url: URL,
  id: number,
  firstName: String,
  lastName: string,
  callName: string,
  email: string,
  phoneNumber: string,
  language: Language,
  extraInfo: string,
  cv: URL,
  portfolio: URL,
  lastEmailSent: Date,
  schoolName: string,
  degree: String,
  studies: string,
  skills: Array<Skill>,
  suggestions: Array<Suggestion>
}

enum Language {
    Dutch = 0,
    English = 1,
    French = 2,
    German = 3,
    Other = 4,
  }
