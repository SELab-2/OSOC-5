import {createRouter, createWebHistory} from 'vue-router'
import SignupForm from "../components/forms/SignupForm.vue";
import LoginForm from "../components/forms/LoginForm.vue";
import NotFoundPage from "../components/NotFoundPage.vue";
import Projects from "../components/appPages/Projects.vue"
import CreateProjects from '../components/appPages/CreateProjects.vue'
import FormPage from "../components/FormPage.vue";
import AppPage from "../components/AppPage.vue";
import UserList from "../components/UserList.vue";
import SelectStudentsPage from "../components/appPages/SelectStudentsPage.vue";
import { hasCsrfToken } from '../utils/axios'



const routes = [
    {
        path: '',
        component: FormPage,
        children: [
            {
                path: 'signup',
                component: SignupForm,
                name: 'Signup'
            },
            {
                path: 'login',
                alias: '',
                component: LoginForm,
                name: "Login"
            },

        ],
    },
    {
        path: '',
        component: AppPage,
        children: [
            {
                path: '/students',
                name: 'Students',
                meta: {
                  requiresAuth: true
                },
                component: SelectStudentsPage
            },
            {
                path: '/projects',
                name: 'Projects',
                meta: {
                  requiresAuth: true
                },
                component: Projects
            },
            {
                path: '/projects/create',
                name: 'Create Project',
                meta: {
                  requiresAuth: true
                },
                component: CreateProjects
            },
            {
                path: '/users',
                name: 'Users',
                meta: {
                  requiresAuth: true
                },
                component: UserList
            },

        ],
    },
    {
        path: "/:catchAll(.*)",
        component: NotFoundPage
    }

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!hasCsrfToken()) {
      next({ name: 'Login' })
    } else {

      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
})

export default router