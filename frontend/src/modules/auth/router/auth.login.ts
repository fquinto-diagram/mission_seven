const routerAuth =[
    {
        path: '/login',
        name: 'login',
        component: ()=>import('@/modules/auth/layouts/PublicLayout.vue'),
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