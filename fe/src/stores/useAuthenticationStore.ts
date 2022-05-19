import axios from 'axios'
import { defineStore } from 'pinia'
import { User, UserInterface } from '../models/User'
import { instance } from '../utils/axios'
import { useStudentStore } from './useStudentStore'
import router from '../router'

const baseURL =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/api/'
    : 'https://sel2-5.ugent.be/api/'

interface State {
  loggedInUser: UserInterface | null
  colorScheme: boolean | 'auto'
}

/**
 * Gets a cookie
 * @param name the name of the cookie
 * @returns the value of the cookie
 */
function getCookie(name: string) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export const useAuthenticationStore = defineStore('user/authentication', {
  persist: true,
  state: (): State => ({
    loggedInUser: null,
    colorScheme: 'auto'
  }),
  actions: {
    /**
     * If we are logged in, we are redirected to /projects
     */
    checkLogin(): void {
      if (
        localStorage.getItem('refreshToken') &&
        localStorage.getItem('accessToken')
      ) {
        router.push({ name: 'Projects' }).then()
      }
    },
    /**
     * Logs us in
     * @param param0 email and password with which we try to log in
     */
    async login({
      email,
      password,
    }: {
      email: string
      password: string
    }): Promise<void> {
      const { data } = await axios.post(baseURL + 'auth/login/', {
        username: email,
        email,
        password,
      })
      localStorage.setItem('refreshToken', data.refresh_token)
      localStorage.setItem('accessToken', data.access_token)
      instance.defaults.headers.common['X-CSRFToken'] = getCookie(
        'csrftoken'
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ) as any
      const result = await instance.get<User>('coaches/' + data.user.pk)
      this.loggedInUser = result.data
    },
    /**
     * Logs us out and cleares the data
     */
    async logout() {
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('accessToken')
      this.loggedInUser = null;
      const studentStore = useStudentStore()
      studentStore.$reset()
      const skillStore = useStudentStore()
      skillStore.$reset()
      const coachStore = useStudentStore()
      coachStore.$reset()
      const projectStore = useStudentStore()
      projectStore.$reset()

      this.$reset()
      router.push({ name: 'Login' }).then()
    },
    /**
     * Changes the password of the currently logged in user
     * @param param0 the new password
     */
    async changePassword({ p1, p2 }: { p1: string; p2: string }) {
      const config = {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      }
      const bodyParameters = {
        new_password1: p1,
        new_password2: p2,
      }
      await axios.post(
        baseURL + 'auth/password/change/',
        bodyParameters,
        config
      )
    },
    /**
     * Registers a new user
     * @param param0 the user information
     */
    async register({
      firstName,
      lastName,
      email,
      password1,
      password2
    }: {
      firstName: string
      lastName: string
      email: string
      password1: string
      password2: string
    }) {
      const config = {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      }
      const bodyParameters = {
        first_name: firstName,
        last_name: lastName,
        username: email,
        email: email,
        password1: password1,
        password2: password2,
      }
      await axios.post(baseURL + 'auth/register/', bodyParameters, config)
    },
  },
})
