import { Project } from './Project'
import { Suggestion } from './Suggestion'

export interface UserInterface {
  id: number
  firstName: string
  lastName: string
  email: string
  isAdmin: boolean
  role: string
  lastEmailSent: Date
  hasProjects: Array<Project>
  suggestions: Array<Suggestion>
}

export class User implements UserInterface {
  id: number
  firstName: string
  lastName: string
  email: string
  isAdmin: boolean
  role: string
  lastEmailSent: Date
  hasProjects: Project[]
  suggestions: Suggestion[]

  constructor(
    id: number,
    firstName: string,
    lastName: string,
    email: string,
    isAdmin: boolean,
    role: string,
    lastEmailSent: Date,
    hasProjects: Project[],
    suggestions: Suggestion[]
  ) {
    this.id = id
    this.firstName = firstName
    this.lastName = lastName
    this.email = email
    this.isAdmin = isAdmin
    this.role = role
    this.lastEmailSent = lastEmailSent
    this.hasProjects = hasProjects
    this.suggestions = suggestions
  }
}
