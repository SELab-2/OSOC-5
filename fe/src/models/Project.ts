import { ProjectDataSkill } from './Skill'
import { Student } from './Student'

export interface ProjectInterface {
  name: string
  partner_name: string
  extra_info: string
  required_skills: Array<ProjectDataSkill>
  coaches: Array<string>
  suggested_students: Array<Student>
}

export class Project implements ProjectInterface {
  name: string
  partner_name: string
  extra_info: string
  required_skills: ProjectDataSkill[]
  coaches: string[]
  suggested_students: Student[]

  constructor(
    name: string,
    partnerName: string,
    extraInfo: string,
    requiredSkills: ProjectDataSkill[],
    coaches: string[],
    suggested_students: Student[]
  ) {
    this.name = name
    this.partner_name = partnerName
    this.extra_info = extraInfo
    this.required_skills = requiredSkills
    this.coaches = coaches
    this.suggested_students = suggested_students
  }
}
