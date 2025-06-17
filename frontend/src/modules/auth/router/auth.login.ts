import { isAuthenticatedGuard } from '../guards/auth.guard'
const routerAuth =[
    {
        path: '/login',
        name: 'login',
        component: ()=>import('@/modules/auth/layouts/PublicLayout.vue'),
        beforeEnter: isAuthenticatedGuard,
        children:[
            {
                path:'',
                name:'login-form',
                component: ()=>import('@/modules/auth/components/MyLogInForm.vue')
            }
        ]
    }
]

export default routerAuth