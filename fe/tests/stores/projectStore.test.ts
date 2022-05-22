import { beforeEach, describe, expect, it, vi} from "vitest";
import { createPinia, setActivePinia } from "pinia";
import axios, { AxiosRequestConfig } from "axios"
import { instance } from '../../src/utils/axios'
import {UrlMockMappingPost, UrlMockMappingGet, UrlMockMappingDelete, UrlMockMappingPatch} from '../mockUrlMappings'
import {useProjectStore} from "../../src/stores/useProjectStore";
import { ProjectSuggestionInterface, TempProjectSuggestion } from "../../src/models/ProjectSuggestion";
import { Project } from "../../src/models/Project";
import { ProjectSkill, TempProjectSkill } from "../../src/models/Skill";
import { UserInterface } from "../../src/models/User";

const getcall_i = vi.spyOn(instance, 'get').mockImplementation((url: string, data?: unknown, config?:
  AxiosRequestConfig<unknown>) => Promise.resolve(JSON.parse(JSON.stringify(UrlMockMappingGet[url]))))
const deletecall_i = vi.spyOn(instance, 'delete').mockImplementation((url: string, data?: unknown, config?:
  AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingDelete[url]))
const postcall_i = vi.spyOn(instance, 'post').mockImplementation((url: string, data?: unknown, config?:
  AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingPost[url]))
const patchcall_i = vi.spyOn(instance, 'patch').mockImplementation((url: string, data?: unknown, config?:
  AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingPatch[url]))

describe("Project Store", () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
    getcall_i.mockClear()
    postcall_i.mockClear()
    deletecall_i.mockClear()
    patchcall_i.mockClear()
  });

  it("fetchSuggestedStudents", async () => {
    
    
    const projectStore = useProjectStore()
    let data = (await instance.get<TempProjectSuggestion>('projects_sug/1')).data
    let result = await projectStore.fetchSuggestedStudents([data])
    expect(result).toHaveLength(1)
    

  })


  it("removeSuggestion", async () => {
    
    const projectStore = useProjectStore()
    let data1 = (await instance.get<ProjectSuggestionInterface>('projects_sug/1')).data
    let data2 = (await instance.get<Project>('projects/1')).data
    await projectStore.removeSuggestion(data2 ,data1)
    expect(postcall_i).toHaveBeenCalledOnce()

  })

  it("addSuggestion", async () => {
    
    const projectStore = useProjectStore()
    await projectStore.addSuggestion(1, "test", "test", "for the lolz")
    expect(postcall_i).toHaveBeenCalledOnce()

  })

  it("getSkill", async () => {
    
    const projectStore = useProjectStore()
    let data = (await instance.get<TempProjectSkill>('proj_skills/1')).data
    let result = await projectStore.getSkill(data)
    expect(result).toBeInstanceOf(ProjectSkill)
    expect(getcall_i).toHaveBeenCalledTimes(2)

  })

  it("getProject", async () => {
    
    const projectStore = useProjectStore()
    let result = await projectStore.getProject(1)
    expect(result).toBeInstanceOf(Project)

  })

  it("getOrFetchProject", async () => {
    
    const projectStore = useProjectStore()
    let result = await projectStore.getOrFetchProject("projects/2/")
    expect(result.name).toBeDefined()

  })

  
  it("loadProject", async () => {
    
    const projectStore = useProjectStore()
    expect(projectStore.projects).toHaveLength(0)
    await projectStore.loadProjects()
    expect(projectStore.projects).toHaveLength(1)

  })

  it("loadNext", async () => {
    
    const projectStore = useProjectStore()
    expect(projectStore.projects).toHaveLength(0)
    await projectStore.loadNext(1, () => true, {"test": "test"})
    expect(projectStore.projects).toHaveLength(1)

  })

  it("receiveSuggestion", async () => {
    
    const projectStore = useProjectStore()
    await projectStore.loadProjects()
    let data = (await instance.get<UserInterface>('coaches/1')).data
    await projectStore.receiveSuggestion({project_id: "1", reason: "test", coach: data, student: 'students/1/', skill: "skills/2"}, 'false')

  })

  it("removeReceivedSuggestion", async () => {
    
    const projectStore = useProjectStore()
    await projectStore.loadProjects()
    await projectStore.removeReceivedSuggestion({project_id: "1", student: 'students/1/', skill: "skills/2"}, 'true')

  })

  it("addProject", async () => {
    
    const projectStore = useProjectStore()
    let data = (await instance.get<Project>('projects/1')).data
    await projectStore.addProject(data)
    let result = expect(postcall_i).toBeCalledTimes(1)
    expect(result).toBeTruthy()
    
  })

  it("updateProject", async () => {
    
    const projectStore = useProjectStore()
    let data = (await instance.get<Project>('projects/1')).data
    await projectStore.updateProject(data, 1)
    expect(patchcall_i).toBeCalledTimes(1)

  })

  it("deleteProject", async () => {
    
    const projectStore = useProjectStore()
    await projectStore.deleteProject(1)
    expect(deletecall_i).toBeCalledTimes(1)

  })

  it("csv", async () => {

    const projectStore = useProjectStore()
    let result = await projectStore.csv()
    expect(result).toBeDefined()
    expect(getcall_i).toHaveBeenCalledTimes(1)
    
})

});