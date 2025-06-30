const routerRoles =[
    {
    path: 'roles',
    name: 'roles',
    children: [
            {
                path: 'form',
                name: 'roles-form',
                component: ()=>import('@/modules/pages/RolesCreate.vue')
            },
            {
                path: 'list',
                name: 'roles-list',
                component: ()=>import('@/modules/pages/RolesList.vue')
            },
            {
                path: 'edit/:id',
                name: 'roles-edit',
                component: ()=>import('@/modules/pages/RolesEdit.vue'),
            }
        ]   

    }
]

export default routerRoles

