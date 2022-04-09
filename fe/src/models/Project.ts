import { Skill } from './Skill'
import { User } from './User'
import { ProjectSuggestion, TempProjectSuggestion } from './ProjectSuggestion'

export interface ProjectInterface {
  name: string
  id: number
  partnerName: string
  extraInfo: string
  requiredSkills: Array<{amount: number, comment: string, skill: Skill}>
  coaches: Array<User>
  suggestedStudents: Array<ProjectSuggestion>
}

export interface TempProject {
  name: string
  id: number
  partnerName: string
  extraInfo: string
  requiredSkills: Array<{amount: number, comment: string, skill: string}>
  coaches: Array<string>
  suggestedStudents: Array<TempProjectSuggestion>
}

export class Project implements ProjectInterface {
  name: string
  partnerName: string
  extraInfo: string
  requiredSkills: {amount: number, comment: string, skill: Skill}[]
  coaches: Array<User>
  suggestedStudents: ProjectSuggestion[]
  id: number
  
  constructor(
    name: string,
    partnerName: string,
    extraInfo: string,
    requiredSkills: {amount: number, comment: string, skill: Skill}[],
    coaches: Array<User>,
    suggested_students: ProjectSuggestion[],
    id: number
  ) {
    this.id = id
    this.name = name
    this.partnerName = partnerName
    this.extraInfo = extraInfo
    this.requiredSkills = requiredSkills
    this.coaches = coaches
    this.suggestedStudents = suggested_students
  }
}
