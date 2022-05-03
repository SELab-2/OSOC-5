import { Skill } from './Skill'
import { User } from './User'
import {
  ProjectSuggestionInterface,
  TempProjectSuggestion,
} from './ProjectSuggestion'

export interface ProjectInterface {
  name: string
  id: number
  partnerName: string
  extraInfo: string
  requiredSkills?: Array<{ amount: number; comment: string; skill: Skill }>
  coaches?: Array<User>
  suggestedStudents?: Array<ProjectSuggestionInterface>
}

export interface TempProject {
  name: string
  id: number
  partnerName: string
  extraInfo: string
  requiredSkills: Array<{ amount: number; comment: string; skill: string }>
  coaches: Array<User>
  suggestedStudents: Array<TempProjectSuggestion>
}

export class Project implements ProjectInterface {
  name: string
  partnerName: string
  extraInfo: string
  requiredSkills?: { amount: number; comment: string; skill: Skill }[]
  coaches?: Array<User>
  suggestedStudents?: ProjectSuggestionInterface[]
  id: number

  constructor(
    name: string,
    partnerName: string,
    extraInfo: string,
    id: number,
    requiredSkills?: { amount: number; comment: string; skill: Skill }[],
    coaches?: Array<User>,
    suggested_students?: ProjectSuggestionInterface[]
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
