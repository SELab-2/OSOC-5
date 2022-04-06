import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'

export interface ProjectInterface {
  name: string
  partnerName: string
  extraInfo: string
  requiredSkills: Array<Skill>
  coaches: Array<User>
  suggested_students: Array<Student>
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
