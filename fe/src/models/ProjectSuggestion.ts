import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'

export interface ProjectSuggestion {
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