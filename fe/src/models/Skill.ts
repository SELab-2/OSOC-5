export interface SkillInterface {
  name: string
  description: string
}

export class Skill implements SkillInterface {
  name: string
  description: string

  constructor(name: string, description: string) {
    this.name = name
    this.description = description
  }
}
