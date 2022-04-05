import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'
import { ProjectSuggestion } from './ProjectSuggestion'

export interface Project {
  name: string
  id: number
  partnerName: string
  extraInfo: string
  requiredSkills: Array<{amount: number, skill: Skill}>
  coaches: Array<User>
  suggestedStudents: Array<ProjectSuggestion>
}
