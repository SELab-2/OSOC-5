import { beforeEach, describe, expect, it, test, vi, assert } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useStudentStore } from "../../src/stores/useStudentStore";
import axios, { AxiosRequestConfig } from "axios"
import { instance } from '../../src/utils/axios'
import {UrlMockMappingPost, UrlMockMappingGet, UrlMockMappingDelete} from '../mockUrlMappings'
import { StudentInterface} from '../../src/models/Student'
import { UserInterface } from '../../src/models/User'

const getcall_i = vi.spyOn(instance, 'get').mockImplementation((url: string, data?: unknown, config?:
    AxiosRequestConfig<unknown>) => Promise.resolve(JSON.parse(JSON.stringify(UrlMockMappingGet[url]))))
const deletecall_i = vi.spyOn(instance, 'delete').mockImplementation((url: string, data?: unknown, config?:
    AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingDelete[url]))
const postcall_i = vi.spyOn(instance, 'post').mockImplementation((url: string, data?: unknown, config?:
    AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingPost[url]))

describe("Project Store", () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
    getcall_i.mockClear()
    deletecall_i.mockClear()
    postcall_i.mockClear()
  });

  it("getStudent", async () => {
    const studentStore = useStudentStore()
    expect(studentStore.students).toHaveLength(0)
    await studentStore.getStudent('students/1/')
    expect(studentStore.students).toHaveLength(1)
  })

  it("yesMaybeNo", async () => {
    const studentStore = useStudentStore()
    expect(studentStore.counts.yes).toBe(0)
    await studentStore.loadYesMaybeNo()
    expect(studentStore.counts.yes).toBe(2)
    expect(studentStore.counts.none).toBe(3)
    expect(getcall_i).toBeCalledTimes(1)
  })

  it("deleteStudent", async () => {
    const studentStore = useStudentStore()
    await studentStore.deleteStudent('students/1/', () => true, () => false)
    expect(deletecall_i).toHaveBeenCalled()
  })

  it("tansformStudent", async () => {
    const studentStore = useStudentStore()
    let data = (await instance.get<StudentInterface>('students/1/')).data
    await studentStore.transformStudent(data)
    expect(getcall_i).toBeCalledTimes(2)
    data.skills[0] = "skills/2"
    await studentStore.transformStudent(data)
    expect(getcall_i).toBeCalledTimes(2)
    expect(data.gender).toBe(1)
  })

  it("loadNext", async () => {
    const studentStore = useStudentStore()
    expect(studentStore.students).toHaveLength(0)
    await studentStore.loadNext(1, () => true, "?test")
    expect(studentStore.students).toHaveLength(1)
  })

  it("loadStudentById", async () => {
    const studentStore = useStudentStore()
    expect(studentStore.currentStudent).toBe(null)
    await studentStore.loadStudent(1, () => console.log("hier"))
    expect(studentStore.currentStudent).toBeDefined()
  })

  it("updateSuggestion", async () => {
    const studentStore = useStudentStore()
    await studentStore.updateSuggestion(1, 1, "test")
    await studentStore.updateSuggestion(1, -1, "remove")
    expect(postcall_i).toHaveBeenCalledTimes(1)
    expect(deletecall_i).toHaveBeenCalledTimes(1)
  })

  it("updateFinalDecision", async () => {
    const studentStore = useStudentStore()
    await studentStore.updateFinalDecision(1, 1, "test")
    await studentStore.updateFinalDecision(1, -1, "remove")
    expect(postcall_i).toHaveBeenCalledTimes(1)
    expect(deletecall_i).toHaveBeenCalledTimes(1)
  })

  it("receiveSuggestion", async () => {
    const studentStore = useStudentStore()
    await studentStore.getStudent('students/1/')
    expect(studentStore.students).toHaveLength(1)
    expect(studentStore.students[0].suggestions).toHaveLength(2)
    var {data} = Object(await instance.get<UserInterface>('coaches/1'))
    await studentStore.receiveSuggestion({student_id: 1, coach: data, suggestion: "0", reason: "test"})
    expect(studentStore.students[0].suggestions).toHaveLength(3)
    var {data} = Object(await instance.get<UserInterface>('coaches/2'))
    await studentStore.receiveSuggestion({student_id: 1, coach: data, suggestion: "0", reason: "test"})
    expect(studentStore.students[0].suggestions).toHaveLength(3)
  })

  it("removeSuggestion", async () => {
    const studentStore = useStudentStore()
    await studentStore.getStudent('students/1/')
    expect(studentStore.students).toHaveLength(1)
    expect(studentStore.students[0].suggestions).toHaveLength(2)
    await studentStore.removeSuggestion({student_id: "1", coach_id: 2})
    expect(studentStore.students[0].suggestions).toHaveLength(1)
  })

  it("receiveFinalDecision", async () => {
    const studentStore = useStudentStore()
    await studentStore.getStudent('students/1/')
    expect(studentStore.students).toHaveLength(1)
    expect(studentStore.students[0].finalDecision).toBeUndefined()
    var {data} = Object(await instance.get<UserInterface>('coaches/1'))
    await studentStore.receiveFinalDecision({student_id: "1", coach: data, suggestion: "0", reason: "test"})
    expect(studentStore.students[0].finalDecision).toBeDefined()
  })

  it("removeFinalDecision", async () => {
    const studentStore = useStudentStore()
    await studentStore.getStudent('students/1/')
    var {data} = Object(await instance.get<UserInterface>('coaches/1'))
    await studentStore.receiveFinalDecision({student_id: "1", coach: data, suggestion: "0", reason: "test"})
    expect(studentStore.students[0].finalDecision).toBeDefined()
    await studentStore.removeFinalDecision({student_id:"1"})
    expect(studentStore.students[0].finalDecision).toBe(null)
  })

});