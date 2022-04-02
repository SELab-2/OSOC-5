import { Skill } from './Skill'
import { Student } from './Student'
import { User } from './User'

export interface Project {
  name: string
  partnerName: string
  extraInfo: string
  requiredSkills: Array<Skill>
  coaches: Array<User>
  suggested_students: Array<Student>
}
