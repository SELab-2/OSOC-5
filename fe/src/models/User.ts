import { Project } from './Project'
import { Suggestion } from './Suggestion'

export interface UserInterface {
  id: number
  url: string
  firstName: string
  lastName: string
  email?: string
  isAdmin?: boolean
  role?: string
  lastEmailSent?: Date
  hasProjects?: Array<Project>
  suggestions?: Array<Suggestion>
  isActive?: boolean
  project: {
    id: number,
    url: String,
    name: string
  }
}

export class User implements UserInterface {
  id: number
  url: string
  firstName: string
  lastName: string
  email?: string
  isAdmin?: boolean
  lastEmailSent?: Date
  hasProjects?: Project[]
  suggestions?: Suggestion[]
  isActive?: boolean
  project: {
    id: number,
    url: String,
    name: string
  }
  
  constructor(data: UserInterface) {
    Object.assign(this, data)
  }

  get fullName(): string {
    return this.firstName + ' ' + this.lastName
  }

  get role(): string {
    return this.isActive ? (this.isAdmin ? 'admin' : 'coach') : 'inactive'
  }

  set role(newRole: string) {
    this.isAdmin = newRole === 'admin'
    this.isActive = newRole !== 'inactive'
  }
}
