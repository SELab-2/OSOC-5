import { createRouter, createWebHistory } from 'vue-router'
import SignupPage from "../components/SignupPage.vue";
import LoginPage from "../components/LoginPage.vue";
import NotFoundPage from "../components/NotFoundPage.vue";

const routes = [
    {
        path: '/signup',
        name: 'Signup',
        component: SignupPage,
    },
    {
        path: '/',
        alias: '/login',
        name: 'Login',
        component: LoginPage,
    },
    {
        path: "/:catchAll(.*)",
        component: NotFoundPage,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
