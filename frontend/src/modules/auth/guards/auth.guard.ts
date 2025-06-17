import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'

export const isAuthenticatedGuard = (
    to: RouteLocationNormalized,
    _from: RouteLocationNormalized,
    next: NavigationGuardNext
) => {
    const token = localStorage.getItem('token')

    if (token) {
        if (to.path === '/login') {
            next({name: 'dashboard'})
            return
        }
    } else {
        if (to.path !== '/login') {
            next({name:'login'})
            return
        }
    }

    next()
}