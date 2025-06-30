import { createRouter, createWebHistory } from 'vue-router'
import routerAuth from '@/modules/auth/router/auth.login'
import routerRoles from '@/modules/roles/routes/roles.routes'
import { isAuthenticatedGuard } from '@/modules/auth/guards/auth.guard'

const routes =[
    {
        path: '/',
        component: ()=>import('@/modules/common/layouts/DefaultLayout.vue'),
        beforeEnter: isAuthenticatedGuard,
        children: [
            {
                path: 'dashboard',
                name: 'dashboard',
                component: ()=>import('@/modules/pages/DashBoard.vue'),

            },
            {
                path: 'profile',
                name: 'profile-form',
                component: ()=>import('@/modules/pages/Profiles.vue')
            },
            ...routerRoles
        ]
    },
    ... routerAuth
]

const router= createRouter({
    history: createWebHistory(),
    routes,
})

export default router