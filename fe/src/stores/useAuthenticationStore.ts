import axios from 'axios'
import { defineStore } from 'pinia'
import { StoreDefinition } from 'pinia'
import { convertObjectKeysToCamelCase } from '../utils/case-conversion'
import { User, UserInterface } from '../models/User'
import {instance} from "../utils/axios";
import {useStudentStore} from "./useStudentStore";
import router from "../router";

const baseURL =
  process.env.NODE_ENV == 'development'
    ? 'http://127.0.0.1:8000/api/'
    : 'https://sel2-5.ugent.be/api/'

interface State {
  loggedInUser: UserInterface | null
}

export const useAuthenticationStore = defineStore('user/authentication', {
  persist: true,
  state: (): State => ({
    loggedInUser: null,
  }),
  actions: {
    checkLogin(): void {
      if (localStorage.getItem('refreshToken') && localStorage.getItem('accessToken')) {
        router.push({name: 'Projects'})
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

      const result = await instance.get<User>('coaches/' + data.user.pk)
      this.loggedInUser = result.data
    },
    async logout() {
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
      router.push({name: 'Login'})
    },
    async changePassword({p1, p2}: 
      {p1: string, p2: string}) {
      const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` }
      };
      const bodyParameters = {
        new_password1: p1,
        new_password2: p2,
      };
      const {data} = await axios.post(baseURL + 'auth/password/change/', bodyParameters, config)
      },
  },
})