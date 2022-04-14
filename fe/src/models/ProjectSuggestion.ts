import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'

export interface ProjectSuggestionInterface {
  student: Student
  coach: User
  skill: Skill
  reason: string
  coachId: number
  coachName: string
}

export interface TempProjectSuggestion {
  student: string
  coach: string
  skill: string
  reason: string
  coachId: number
  coachName: string
}

export class ProjectSuggestion implements ProjectSuggestionInterface {
  student: Student
  coach: User
  skill: Skill
  reason: string
  coachId: number
  coachName: string
  
  constructor(data: ProjectSuggestionInterface) {
    Object.assign(this, data)
  }
}