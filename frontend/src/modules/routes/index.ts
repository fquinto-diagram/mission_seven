import { createRouter, createWebHistory } from 'vue-router'
import routerAuth from '../auth/router/auth.login'
import { isAuthenticatedGuard } from '../auth/guards/auth.guard'
const routes =[
    {
        path: '/',
        component: ()=>import('@/modules/layouts/DefaultLayout.vue'),
        beforeEnter: isAuthenticatedGuard,
        children: [
            {
                path: '',
                name: 'dashboard',
                component: ()=>import('@/modules/common/pages/DashBoard.vue'),

            }

        ]
    },
    ... routerAuth
]

const router= createRouter({
    history: createWebHistory(),
    routes,
})

export default router