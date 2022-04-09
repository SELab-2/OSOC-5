export interface SkillInterface {
  name: string
  description: string
  url: string
}

export class Skill implements SkillInterface {
  name: string
  description: string
  url: string
  constructor(name: string, description: string, url: string) {
    this.name = name
    this.description = description
    this.url = url
  }
}

export interface TempProjectSkill {
  amount: number
  comment: string
  skill: string
}

export interface ProjectSkill {
  amount: number
  comment: string
  skill: Skill
}
