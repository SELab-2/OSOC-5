import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'
import { ProjectSuggestion } from './ProjectSuggestion'

export interface ProjectInterface {
  name: string
  id: number
  partnerName: string
  extraInfo: string
  requiredSkills: Array<{amount: number, comment: string, skill: Skill}>
  coaches: Array<User>
  suggestedStudents: Array<ProjectSuggestion>
}

export class Project implements ProjectInterface {
  name: string
  partnerName: string
  extraInfo: string
  requiredSkills: {amount: number, comment: string, skill: Skill}[]
  coaches: User[]
  suggestedStudents: ProjectSuggestion[]
  id: number
  
  constructor(
    name: string,
    partnerName: string,
    extraInfo: string,
    requiredSkills: {amount: number, comment: string, skill: Skill}[],
    coaches: User[],
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

export class Project implements ProjectInterface {
  name: string
  partnerName: string
  extraInfo: string
  requiredSkills: Skill[]
  coaches: User[]
  suggested_students: Student[]

  constructor(
    name: string,
    partnerName: string,
    extraInfo: string,
    requiredSkills: Skill[],
    coaches: User[],
    suggested_students: Student[]
  ) {
    this.name = name
    this.partnerName = partnerName
    this.extraInfo = extraInfo
    this.requiredSkills = requiredSkills
    this.coaches = coaches
    this.suggested_students = suggested_students
  }
}
