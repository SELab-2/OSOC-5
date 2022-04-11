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
  
  constructor(obj: SkillInterface);
  constructor(name: string, id: number, color: string, url: string);
  constructor(...args: any[]) {
    if (args.length == 1) {
      Object.assign(this, args[0])
    } else {
      this.name = args[0]
      this.id = args[1]
      this.color = args[2]
      this.url = args[3]
    } 
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