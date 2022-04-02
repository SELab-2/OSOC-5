import { Project } from './Project'
import { Suggestion } from './Suggestion'

export interface User {
  id: string
  firstName: string
  surname: string
  email: string
  isAdmin: boolean
  role: string
  lastEmailSent: Date
  has_projects: Array<Project>
  suggestions: Array<Suggestion>
}
