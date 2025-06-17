import { createRouter, createWebHistory } from 'vue-router'
import routerAuth from '../auth/router/auth.login'

const routes =[
    {
        path: '/',
        component: ()=>import('@/modules/layouts/DefaultLayout.vue'),
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