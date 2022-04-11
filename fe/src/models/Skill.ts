import { Url } from 'url'

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

export interface TempProjectSkill {
  amount: number
  comment: string
  skill: string
}

export interface ProjectSkill {
  amount: number
  comment: string
  skill: Skill | string
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
