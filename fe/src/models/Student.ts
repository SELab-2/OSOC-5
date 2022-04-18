import { Skill } from './Skill'
import { Suggestion } from './Suggestion'

export interface TempStudent {
  student: string
  coach: string
  skill: string
  reason: string
}

export interface StudentInterface {
  url: string
  id: number
  firstName: string
  lastName: string
  callName: string
  email: string
  phoneNumber: string
  language: number
  motivation: string
  cv: URL
  portfolio: URL
  lastEmailSent: Date
  schoolName: string
  degree: string
  studies: string
  skills: Array<Skill> | Array<string>
  finalDecision: Suggestion | null
  suggestions: Array<Suggestion>
  alum: boolean
  bestSkill: string
  degreeCurrentYear: number
  degreeDuration: number
  employmentAgreement: string
  englishRating: number
  funFact: string
  gender: number
  hinderWork: string
  pronouns: string
  studentCoach: boolean
}

export class Student implements StudentInterface {
  url: string
  id: number
  firstName: string
  lastName: string
  callName: string
  email: string
  phoneNumber: string
  language: number
  motivation: string
  cv: URL
  portfolio: URL
  lastEmailSent: Date
  schoolName: string
  degree: string
  studies: string
  skills: Skill[] | string[]
  finalDecision: Suggestion | null
  suggestions: Suggestion[]
  alum: boolean
  bestSkill: string
  degreeCurrentYear: number
  degreeDuration: number
  employmentAgreement: string
  englishRating: number
  funFact: string
  gender: number
  hinderWork: string
  pronouns: string
  studentCoach: boolean

  constructor(obj: StudentInterface);
  constructor(
    url: string,
    id: number,
    firstName: string,
    lastName: string,
    callName: string,
    email: string,
    phoneNumber: string,
    language: number,
    motivation: string,
    cv: URL,
    portfolio: URL,
    lastEmailSent: Date,
    schoolName: string,
    degree: string,
    studies: string,
    skills: Skill[],
    finalDecision: Suggestion | null,
    suggestions: Suggestion[],
    alum: boolean,
    bestSkill: string,
    degreeCurrentYear: number,
    degreeDuration: number,
    employmentAgreement: string,
    englishRating: number,
    funFact: string,
    gender: number,
    hinderWork: string,
    pronouns: string,
    studentCoach: boolean
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
      this.motivation = args[8]
      this.cv = args[9]
      this.portfolio = args[10]
      this.lastEmailSent = args[11]
      this.schoolName = args[12]
      this.degree = args[13]
      this.studies = args[14]
      this.skills = args[15]
      this.finalDecision = args[16]
      this.suggestions = args[17]
      this.alum = args[18]
      this.bestSkill = args[19]
      this.degreeCurrentYear = args[20]
      this.degreeDuration = args[21]
      this.employmentAgreement = args[22]
      this.englishRating = args[23]
      this.funFact = args[24]
      this.gender = args[25]
      this.hinderWork = args[26]
      this.pronouns = args[27]
      this.studentCoach = args[28]
    }
  }

  get fullName(): string {
    return this.firstName + " " + this.lastName;
  }

  get status(): string {
    return '0'
  }
}
