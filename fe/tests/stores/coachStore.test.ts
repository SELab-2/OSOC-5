import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useCoachStore } from "../../src/stores/useCoachStore";
import { useAuthenticationStore } from "../../src/stores/useAuthenticationStore";
import axios, { AxiosRequestConfig } from "axios"
import { instance } from '../../src/utils/axios'
import {UrlMockMappingDelete, UrlMockMappingPut, UrlMockMappingGet} from '../mockUrlMappings'
import { User, UserInterface } from '../../src/models/User'

const baseURL = "https://sel2-5.ugent.be/api/";

const getcall_i = vi.spyOn(instance, 'get').mockImplementation((url: string, data?: unknown, config?:
  AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingGet[url]))

const putcall_i = vi.spyOn(instance, 'put').mockImplementation((url: string, data?: unknown, config?:
  AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingPut[url]))

const deletecall_i = vi.spyOn(instance, 'delete').mockImplementation((url: string, data?: unknown, config?:
  AxiosRequestConfig<unknown>) => Promise.resolve(UrlMockMappingDelete[url]))

describe("Coach Store", () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
    putcall_i.mockClear()
    getcall_i.mockClear()
  });

  it("getUser", async () => {

    const coachStore = useCoachStore();
    const authenticationStore = useAuthenticationStore()
    authenticationStore.loggedInUser = {id: 1, role: "nope", url: "coaches/1", firstName: "test", lastName: "test", email: "test", isAdmin: true, isActive: true}
    let fetchedUser = {id: 1, role: "nope", url: "coaches/1", firstName: "test", lastName: "test", email: "test", isAdmin: true, isActive: true}
    let result = await coachStore.getUser(fetchedUser)
    expect(result.id).toBeDefined()
    expect(getcall_i).toHaveBeenCalledOnce()

  });

  it("loadUsers", async () => {

    const coachStore = useCoachStore();
    expect(coachStore.users).toHaveLength(0)
    expect(coachStore.isLoading).toBe(false);
    await coachStore.loadUsers()
    expect(coachStore.users).toHaveLength(1)

  });

  it("updateRole", async () => {

    const coachStore = useCoachStore();
    let fetchedUser = {id: 1, role: "nope", url: "coaches/1", firstName: "test", lastName: "test", email: "test", isAdmin: true, isActive: true} as User
    await coachStore.updateRole(await coachStore.getUser(fetchedUser))
    expect(putcall_i).toHaveBeenCalledOnce()

  });

  it("removeUser", async () => {
    
    const coachStore = useCoachStore();
    expect(coachStore.users).toHaveLength(0)
    await coachStore.loadUsers()
    expect(coachStore.users).toHaveLength(1)
    await coachStore.removeUser(1, () => true, () => false)
    expect(deletecall_i).toHaveBeenCalledOnce()

  });

  it("clearStorage", async () => {

    const coachStore = useCoachStore();
    await coachStore.loadUsers()
    expect(coachStore.users).toHaveLength(1)
    coachStore.clearUsers()
    expect(coachStore.users).toHaveLength(0)
    
  })

  it("loadUserCoaches", async () => {

    const coachStore = useCoachStore();
    expect(coachStore.isLoading).toBe(false)
    expect(coachStore.users).toHaveLength(0)
    await coachStore.loadUsersCoaches({'test': 'test'}, (c: number) => true)
    expect(coachStore.users).toHaveLength(1)
  })
});