export interface SkillInterface {
  name: string
  description: string
  url: URL
}

export class Skill implements SkillInterface {
  name: string
  description: string

  constructor(name: string, description: string) {
    this.name = name
    this.description = description
  }
}
