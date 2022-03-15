import {createRouter, createWebHistory} from 'vue-router'
import SignupPage from "../components/formPages/SignupPage.vue";
import LoginPage from "../components/formPages/LoginPage.vue";
import NotFoundPage from "../components/NotFoundPage.vue";
import Example from "../components/appPages/Example.vue"
import Example2 from "../components/appPages/Example2.vue"
import Example3 from "../components/appPages/Example3.vue"
import FormPage from "../components/FormPage.vue";
import AppPage from "../components/AppPage.vue";


const routes = [
    {
        path: '',
        component: FormPage,
        children: [
            {
                path: 'signup',
                component: SignupPage
            },
            {
                path: 'login',
                alias: '',
                component: LoginPage
            },

        ],
    },
    {
        path: '',
        component: AppPage,
        children: [
            {
                path: '/example',
                name: 'Example',
                component: Example
            },
            {
                path: '/example2',
                name: 'Example2',
                component: Example2
            },
            {
                path: '/example3',
                name: 'Example3',
                component: Example3
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
