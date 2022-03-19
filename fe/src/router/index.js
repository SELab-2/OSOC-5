import {createRouter, createWebHistory} from 'vue-router'
import SignupForm from "../components/forms/SignupForm.vue";
import LoginForm from "../components/forms/LoginForm.vue";
import NotFoundPage from "../components/NotFoundPage.vue";
import Example2 from "../components/appPages/Example2.vue"
import FormPage from "../components/FormPage.vue";
import AppPage from "../components/AppPage.vue";
import UserList from "../components/UserList.vue";
import SelectStudentsPage from "../components/appPages/SelectStudentsPage.vue";


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
                component: SelectStudentsPage
            },
            {
                path: '/example2',
                name: 'Example2',
                component: Example2
            },
            {
                path: '/users',
                name: 'Users',
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

export default router