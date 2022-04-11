import { Skill } from './Skill'
import { Suggestion } from './Suggestion'

export interface StudentInterface {
  url: URL
  id: number
  firstName: string
  lastName: string
  callName: string
  email: string
  phoneNumber: string
  language: Language
  extraInfo: string
  cv: URL
  portfolio: URL
  lastEmailSent: Date
  schoolName: string
  degree: string
  studies: string
  skills: Array<Skill>
  finalDecision: Suggestion | null
  suggestions: Array<Suggestion>
}

enum Language {
  Dutch = 0,
  English = 1,
  French = 2,
  German = 3,
  Other = 4,
}

export class Student implements StudentInterface {
  url: URL
  id: number
  firstName: string
  lastName: string
  callName: string
  email: string
  phoneNumber: string
  language: Language
  extraInfo: string
  cv: URL
  portfolio: URL
  lastEmailSent: Date
  schoolName: string
  degree: string
  studies: string
  skills: Skill[]
  finalDecision: Suggestion | null
  suggestions: Suggestion[]

  constructor(obj: StudentInterface);
  constructor(
    url: URL,
    id: number,
    firstName: string,
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
    degree: string,
    studies: string,
    skills: Skill[],
    finalDecision: Suggestion | null,
    suggestions: Suggestion[]
  );

  constructor (...args: any[]) {
    if (args.length == 1) {
      Object.assign(this, args[0])
    } else {
      this.url = args[0]
      this.id = args[1]
      this.firstName = args[2]
      this.lastName = args[3]
      this.callName = args[4]
      this.email = args[5]
      this.phoneNumber = args[6]
      this.language = args[7]
      this.extraInfo = args[8]
      this.cv = args[9]
      this.portfolio = args[10]
      this.lastEmailSent = args[11]
      this.schoolName = args[12]
      this.degree = args[13]
      this.studies = args[14]
      this.skills = args[15]
      this.finalDecision = args[16]
      this.suggestions = args[17]
    }
  }
}
