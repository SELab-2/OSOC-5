export interface SkillInterface {
  name: string
  description: string // TODO REMOVE ON DATABASE UPDATE ISSUE #110
  url: string
  id: number
}

export class Skill implements SkillInterface {
  name: string
  description: string
  url: string
  id: number

  constructor(name: string, description: string, url: string, id: number) {
    this.name = name
    this.description = description
    this.url = url
    this.id = id
  }
}

export class ProjectSkill extends Skill {
  amount: number
  comment: string

  constructor(
    name: string,
    description: string,
    url: string,
    id: number,
    amount: number,
    comment: string
  ) {
    super(name, description, url, id)
    this.amount = amount
    this.comment = comment
  }
}

export class ProjectDataSkill {
  skill: string
  amount: number
  // comment: string TODO ADD ON DATABASE UPDATE ISSUE #110

  constructor(skill: string, amount: number, /*comment: string*/) {
    this.skill = skill
    this.amount = amount
    // this.comment = comment
  }
}