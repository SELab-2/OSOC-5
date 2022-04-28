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
}

function getCookie(name: String) {
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
  }),
  actions: {
    checkLogin(): void {
      if (
        localStorage.getItem('refreshToken') &&
        localStorage.getItem('accessToken')
      ) {
        router.push({ name: 'Projects' }).then()
      }
    },
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
      instance.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken') as any
      const result = await instance.get<User>('coaches/' + data.user.pk)
      this.loggedInUser = result.data
    },
    logout(): void {
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('accessToken')

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
  },
})
