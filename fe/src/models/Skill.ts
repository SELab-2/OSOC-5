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

export class ProjectSkill implements ProjectSkillInterface {
  amount: number
  comment: string
  skill: Skill
  
  constructor(obj: ProjectSkillInterface);
  constructor(amount: number, comment: string, skill: Skill);
  constructor(...args: any[]) {
    if (args.length == 1) {
      Object.assign(this, args[0])
    } else {
      this.amount = args[0]
      this.comment = args[1]
      this.skill = args[2]
    } 
  }
}

export interface TempProjectSkill {
  amount: number
  comment: string
  skill: string
}

export interface ProjectSkillInterface {
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