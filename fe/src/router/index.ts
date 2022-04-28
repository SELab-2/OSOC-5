import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import AppPageVue from '../components/AppPage.vue'
import FormPageVue from '../features/authentication/FormPage.vue'
import LoginFormVue from '../features/authentication/LoginForm.vue'
import SelectStudentsPageVue from '../features/students/SelectStudentsPage.vue'
import StudentPage from '../features/students/StudentPage.vue'
import ProjectList from '../features/projects/ProjectList.vue'
import CreateProjects from '../features/projects/CreateProject.vue'
import UserList from '../features/users/UserList.vue'
import NotFoundPage from '../components/NotFoundPage.vue'
import {useStudentStore} from "../stores/useStudentStore";

const routes: Array<RouteRecordRaw> = [
  {
    path: '',
    component: FormPageVue,
    children: [
      {
        path: 'login',
        alias: '',
        component: LoginFormVue,
        name: 'Login',
      },
    ],
  },
  {
    path: '',
    component: AppPageVue,
    children: [
      {
        path: '/students',
        name: 'Students',
        meta: {
          requiresAuth: true,
        },
        component: SelectStudentsPageVue,
      },
      {
        path: '/students/:id',
        name: 'Student Page',
        meta: {
          requiresAuth: true,
        },
        props: true,
        component: StudentPage,
      },
      {
        path: '/projects',
        name: 'Projects',
        meta: {
          requiresAuth: true,
        },
        component: ProjectList,
      },
      {
        path: '/projects/create',
        name: 'Create Project',
        meta: {
          requiresAuth: true,
        },
        component: CreateProjects,
      },
      {
        path: '/users',
        name: 'Users',
        meta: {
          requiresAuth: true,
        },
        component: UserList,
      },
    ],
  },
  {
    path: '/:catchAll(.*)',
    component: NotFoundPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const studentStore = useStudentStore()
  studentStore.currentStudent = null

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!localStorage.getItem('accessToken')) {
      next({ name: 'Login' })
    } else {
      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
})

export default router
