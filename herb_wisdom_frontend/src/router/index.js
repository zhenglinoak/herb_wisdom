import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/login',
        name: 'login',
        component: () => import('../components/Login.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('../components/Register.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/chat',
        name: 'chat',
        component: () => import('../components/Chat.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/search',
        name: 'search',
        component: () => import('../components/Search.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/chat'
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const token = sessionStorage.getItem('token')
    const userName = sessionStorage.getItem('userName')
    const isAuthenticated = !!(token && userName)

    if (to.path === '/login') {
        sessionStorage.clear()
        return next()
    }

    if (to.meta.requiresAuth && !isAuthenticated) {
        return next({ path: '/login' })
    }

    if (!to.meta.requiresAuth && isAuthenticated && (to.path === '/login' || to.path === '/register')) {
        return next({ path: '/chat' })
    }

    next()
})

export default router