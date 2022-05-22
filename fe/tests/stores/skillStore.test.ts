import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useSkillStore } from '../../src/stores/useSkillStore'
import { AxiosRequestConfig } from 'axios'
import { instance } from '../../src/utils/axios'
import {
  UrlMockMappingGet,
  UrlMockMappingPost,
  UrlMockMappingPatch,
  UrlMockMappingDelete,
} from '../mockUrlMappings'
import { SkillInterface } from '../../src/models/Skill'

const getcall_i = vi
  .spyOn(instance, 'get')
  .mockImplementation(
    (url: string, data?: unknown, config?: AxiosRequestConfig<unknown>) =>
      Promise.resolve(JSON.parse(JSON.stringify(UrlMockMappingGet[url])))
  )
const postcall_i = vi
  .spyOn(instance, 'post')
  .mockImplementation(
    (url: string, data?: unknown, config?: AxiosRequestConfig<unknown>) =>
      Promise.resolve(UrlMockMappingPost[url])
  )
const patchcall_i = vi
  .spyOn(instance, 'patch')
  .mockImplementation(
    (url: string, data?: unknown, config?: AxiosRequestConfig<unknown>) =>
      Promise.resolve(UrlMockMappingPatch[url])
  )
const deletecall_i = vi
  .spyOn(instance, 'delete')
  .mockImplementation(
    (url: string, data?: unknown, config?: AxiosRequestConfig<unknown>) =>
      Promise.resolve(UrlMockMappingDelete[url])
  )

describe('Skill Store', () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia())
    getcall_i.mockClear()
    postcall_i.mockClear()
    deletecall_i.mockClear()
    patchcall_i.mockClear()
  })

  it('getSkill', async () => {
    const skillStore = useSkillStore()
    expect(skillStore.skills).toHaveLength(0)
    await skillStore.getSkill('skills/2')
    expect(skillStore.skills).toHaveLength(1)
  })

  it('loadSkills', async () => {
    const skillStore = useSkillStore()
    expect(skillStore.skills).toHaveLength(0)
    await skillStore.loadSkills()
    expect(skillStore.skills).toHaveLength(2)
  })

  it('loadNext', async () => {
    const skillStore = useSkillStore()
    expect(skillStore.skills).toHaveLength(0)
    await skillStore.loadNext(1, () => true, '?test')
    expect(skillStore.skills).toHaveLength(2)
  })

  it('addSkill', async () => {
    const skillStore = useSkillStore()
    expect(skillStore.skills).toHaveLength(0)
    const data = (await instance.get<SkillInterface>('skills/2')).data
    await skillStore.addSkill(data, () => true)
    expect(skillStore.skills).toHaveLength(1)
    expect(postcall_i).toHaveBeenCalledTimes(1)
  })

  it('updateSkill', async () => {
    const skillStore = useSkillStore()
    const data = (await instance.get<SkillInterface>('skills/2')).data
    skillStore.updateSkill(data, () => true)
    expect(patchcall_i).toHaveBeenCalledTimes(1)
  })

  it('deleteSkill', async () => {
    const skillStore = useSkillStore()
    const data = (await instance.get<SkillInterface>('skills/2')).data
    await skillStore.addSkill(data, () => true)
    expect(skillStore.skills).toHaveLength(1)
    await skillStore.deleteSkill(1, () => true)
    expect(skillStore.skills).toHaveLength(0)
  })

  it('csv', async () => {
    const skillStore = useSkillStore()
    const result = await skillStore.csv()
    expect(result).toBeDefined()
    expect(getcall_i).toHaveBeenCalledTimes(1)
  })
})
