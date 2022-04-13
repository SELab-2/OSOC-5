import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'

export interface ProjectSuggestionInterface {
  student: Student
  coach: User
  skill: Skill
  reason: string
}

export interface TempProjectSuggestion {
  student: string
  coach: string
  skill: string
  reason: string
}

export class ProjectSuggestion implements ProjectSuggestionInterface {
  student: Student
  coach: User
  skill: Skill
  reason: string
  
  constructor(data: ProjectSuggestionInterface) {
    Object.assign(this, data)
  }
}