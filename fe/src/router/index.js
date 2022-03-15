import { createRouter, createWebHistory } from 'vue-router'
import SignupPage from "../components/SignupPage.vue";
import LoginPage from "../components/LoginPage.vue";
import NotFoundPage from "../components/NotFoundPage.vue";
import Example from "../components/Example.vue"
import Example2 from "../components/Example2.vue"
import Example3 from "../components/Example3.vue"


const routes = [
    {
        path: '/signup',
        name: 'Signup',
        component: SignupPage
    },
    {
        path: '/',
        alias: '/login',
        name: 'Login',
        component: LoginPage
    },
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
    {
        path: "/:catchAll(.*)",
        component: NotFoundPage
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
