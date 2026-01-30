import { createRouter, createWebHistory } from 'vue-router'
import JobList from '../components/JobList.vue'
import Login from '../views/Login.vue'
import api from '../services/api'

const routes = [
    {
        path: '/',
        component: JobList,
        meta: { requiresAuth: true }
    },
    {
        path: '/login',
        component: Login
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAuth) {
        try {
            const auth = await api.checkAuth();
            if (!auth.authenticated) {
                next('/login');
            } else {
                next();
            }
        } catch (e) {
            next('/login');
        }
    } else {
        // If going to login while authenticated, redirect to home
        if (to.path === '/login') {
            const auth = await api.checkAuth();
            if (auth.authenticated) {
                next('/');
                return;
            }
        }
        next();
    }
})

export default router
