import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useProjectConflictStore } from '../../src/stores/useProjectConflictStore'
import { AxiosRequestConfig } from 'axios'
import { instance } from '../../src/utils/axios'
import {
  UrlMockMappingGet,
  UrlMockMappingPost,
  UrlMockMappingPatch,
  UrlMockMappingDelete,
} from '../mockUrlMappings'
import { StudentInterface, Student } from '../../src/models/Student'

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
    patchcall_i.mockClear()
    deletecall_i.mockClear()
  })

  it('getConflictingProjects', async () => {
    const projectConflictStore = useProjectConflictStore()
    await projectConflictStore.getConflictingProjects()
    expect(projectConflictStore.conflicts).toHaveLength(1)
  })

  it('resolveConflict', async () => {
    const projectConflictStore = useProjectConflictStore()
    await projectConflictStore.getConflictingProjects()
    const project = projectConflictStore.conflicts[0]
    const errortest = project.projects[0].suggestedStudents[0]
    errortest.student = new Student(
      (await instance.get<StudentInterface>('students/1/')).data
    )
    project.projects[0].suggestedStudents = []
    // Should not pass since there are no suggested students
    await expect(
      async () =>
        await projectConflictStore.resolveConflict(project.projects[0], project)
    ).rejects.toThrow(/unexpected/)
    project.projects[0].suggestedStudents = [errortest, errortest]
    // Should not pass since there are multiple suggested students with the same id
    await expect(
      async () =>
        await projectConflictStore.resolveConflict(project.projects[0], project)
    ).rejects.toThrow(/delete/)
    project.projects[0].suggestedStudents = [errortest]
    // Should pass
    await projectConflictStore.resolveConflict(project.projects[0], project)
  })
})
