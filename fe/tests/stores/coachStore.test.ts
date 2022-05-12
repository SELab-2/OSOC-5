import { beforeEach, describe, expect, it, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useCoachStore } from "../../src/stores/useCoachStore";
import axios, { AxiosRequestConfig } from "axios"
import { instance } from '../../src/utils/axios'
import {UrlMockMappingDelete, UrlMockMappingPut, UrlMockMappingGet} from '../mockUrlMappings'

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
    let result = await coachStore.getUser("coaches/1")
    expect(getcall_i).toHaveBeenCalledOnce()
    expect(result.id).toBeDefined()

  });

  it("loadUsers", async () => {

    const coachStore = useCoachStore();
    expect(coachStore.users).toHaveLength(0)
    expect(coachStore.isLoadingUsers).toBe(false);
    await coachStore.loadUsers()
    expect(coachStore.users).toHaveLength(1)

  });

  it("updateRole", async () => {

    const coachStore = useCoachStore();
    await coachStore.updateRole(await coachStore.getUser("coaches/1"))
    expect(putcall_i).toHaveBeenCalledOnce()

  });

  it("removeUser", async () => {
    
    const coachStore = useCoachStore();
    expect(coachStore.users).toHaveLength(0)
    await coachStore.loadUsers()
    expect(coachStore.users).toHaveLength(1)
    await coachStore.removeUser(1)
    expect(coachStore.users).toHaveLength(0)
    expect(deletecall_i).toHaveBeenCalledOnce()

  });

  it("clearStorage"), async () => {

    const coachStore = useCoachStore();
    await coachStore.loadUsers()
    expect(coachStore.users).toHaveLength(1)
    coachStore.clearUsers()
    expect(coachStore.users).toHaveLength(0)
    
  }

});