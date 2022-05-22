/**
 * @vitest-environment jsdom
 */
import { beforeEach, describe, expect, it, test, vi, assert } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthenticationStore } from '../../src/stores/useAuthenticationStore'
import axios, { AxiosRequestConfig } from 'axios'
import { instance } from '../../src/utils/axios'
import { UrlMockMappingPost, UrlMockMappingGet } from '../mockUrlMappings'
import router from '../../src/router'

const postcall = vi
  .spyOn(axios, 'post')
  .mockImplementation(
    (url: string, data?: unknown, config?: AxiosRequestConfig<unknown>) =>
      Promise.resolve(UrlMockMappingPost[url.split('api/')[1]])
  )
const getcall_i = vi
  .spyOn(instance, 'get')
  .mockImplementation(
    (url: string, data?: unknown, config?: AxiosRequestConfig<unknown>) =>
      Promise.resolve(UrlMockMappingGet[url])
  )

describe('authenticationStore', () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia())
    postcall.mockClear()
    getcall_i.mockClear()
  })

  it('changepassword', async () => {
    const authenticationStore = useAuthenticationStore()
    await authenticationStore.changePassword({
      p1: 'test',
      p2: 'test',
    })
    expect(postcall).toHaveBeenCalledOnce()
  })

  it('login', async () => {
    const authenticationStore = useAuthenticationStore()
    await authenticationStore.login({ username: 'test', password: 'test2' })
    expect(localStorage.getItem('accessToken')).toBe('fresh')
    expect(localStorage.getItem('refreshToken')).toBe('funky')
    expect(postcall).toHaveBeenCalledOnce()
    expect(getcall_i).toHaveBeenCalledOnce()
    expect(authenticationStore.loggedInUser.isActive).toBeTruthy()
  })

  it('logout', async () => {
    const authenticationStore = useAuthenticationStore()
    localStorage.setItem('refreshToken', 'test')
    await authenticationStore.logout()
    expect(localStorage.getItem('refreshToken')).toBeNull()
  })

  it('register', async () => {
    const authenticationStore = useAuthenticationStore()
    await authenticationStore.register({
      firstName: 'me',
      lastName: 'too',
      email: 'example@address.com',
      password1: 'admin',
      password2: 'admin',
      is_admin: true,
      is_active: true,
    })
    expect(postcall).toHaveBeenCalledOnce()
  })

  it('checkLogin', async () => {
    const spyRouter = vi.spyOn(router, 'push')
    const authenticationStore = useAuthenticationStore()
    localStorage.setItem('refreshToken', 'test')
    localStorage.setItem('accessToken', 'test')
    await authenticationStore.checkLogin()
    expect(spyRouter).toHaveBeenCalledOnce()
  })
})
