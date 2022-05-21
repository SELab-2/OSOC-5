import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'

export interface ProjectSuggestionInterface {
  student: Student
  coach?: User
  skill: Skill
  reason: string
  coachId?: number
  coachName?: string
}

export interface TempProjectSuggestion {
  student: string
  coach?: User
  skill: string
  reason: string
  coachId: number
  coachName: string
}

export class ProjectSuggestion implements ProjectSuggestionInterface {
  student: Student
  coach?: User
  skill: Skill
  reason: string
  coachId?: number
  coachName?: string

  constructor(data: ProjectSuggestionInterface) {
    Object.assign(this, data)
  }
}

// Extra class to differentiate new suggestions from existing suggestions.
export class NewProjectSuggestion extends ProjectSuggestion {
  fromWebsocket: boolean
  fromLocal: boolean

  constructor(data: ProjectSuggestionInterface, fromWebsocket: boolean) {
    super(data)
    this.fromWebsocket = fromWebsocket
    this.fromLocal = !fromWebsocket
  }
}
