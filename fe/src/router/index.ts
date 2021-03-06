import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import AppPageVue from '../components/AppPage.vue'
import FormPageVue from '../features/authentication/FormPage.vue'
import LoginFormVue from '../features/authentication/LoginForm.vue'
import SelectStudentsPageVue from '../features/students/SelectStudentsPage.vue'
import StudentPage from '../features/students/StudentPage.vue'
import ProjectList from '../features/projects/ProjectList.vue'
import ResolveConflicts from '../features/projects/ResolveConflicts.vue'
import CreateProject from '../features/projects/CreateProject.vue'
import UserList from '../features/users/UserList.vue'
import MailList from '../features/mails/MailList.vue'
import NotFoundPage from '../components/NotFoundPage.vue'
import AdvancedPage from '../components/AdvancedPage.vue'

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
        path: '/projects/:id',
        name: 'Project Page',
        meta: {
          requiresAuth: true,
        },
        props: true,
        component: CreateProject,
      },
      {
        path: '/projects/create',
        name: 'Create Project',
        meta: {
          requiresAuth: true,
        },
        component: CreateProject,
      },
      {
        path: '/projects/conflicts',
        name: 'Project Conflicts',
        meta: {
          requiresAuth: true,
        },
        component: ResolveConflicts,
      },
      {
        path: '/users',
        name: 'Users',
        meta: {
          requiresAuth: true,
        },
        component: UserList,
      },
      {
        path: '/mails',
        name: 'Mails',
        meta: {
          requiresAuth: true,
        },
        component: MailList,
      },
      {
        path: '/advanced',
        name: 'Advanced',
        meta: {
          requiresAuth: true,
        },
        component: AdvancedPage,
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
