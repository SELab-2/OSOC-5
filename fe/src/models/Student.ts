import { Skill } from './Skill'
import { Suggestion } from './Suggestion'

export interface TempStudent {
  student: string
  coach: string
  skill: string
  reason: string
}

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
  ) {
    this.url = url
    this.id = id
    this.firstName = firstName
    this.lastName = lastName
    this.callName = callName
    this.email = email
    this.phoneNumber = phoneNumber
    this.language = language
    this.extraInfo = extraInfo
    this.cv = cv
    this.portfolio = portfolio
    this.lastEmailSent = lastEmailSent
    this.schoolName = schoolName
    this.degree = degree
    this.studies = studies
    this.skills = skills
    this.finalDecision = finalDecision
    this.suggestions = suggestions
  }
}
