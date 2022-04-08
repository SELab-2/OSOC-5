export interface SkillInterface {
  name: string
  id: number
  color: string
  url: string
}

export class Skill implements SkillInterface {
  name: string
  id: number
  color: string
  url: string

  constructor(name: string, id: number, color: string, url: string) {
    this.name = name
    this.id = id
    this.color = color
    this.url = url
  }
}

export class ProjectTableSkill implements SkillInterface {
  name: string
  id: number
  color: string
  url: string
  amount: number
  comment: string

  constructor(
    name: string,
    id: number,
    color: string,
    url: string,
    amount: number,
    comment: string
  ) {
    this.name = name
    this.id = id
    this.color = color
    this.url = url
    this.amount = amount
    this.comment = comment
  }
}

export class ProjectSkill {
  skill: string
  amount: number
  comment: string

  constructor(skill: string, amount: number, comment: string) {
    this.skill = skill
    this.amount = amount
    this.comment = comment
  }
}