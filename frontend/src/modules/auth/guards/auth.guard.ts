import { useCookies } from 'vue3-cookies';
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router';

const { cookies } = useCookies();

export const isAuthenticatedGuard = (
    to: RouteLocationNormalized,
    _from: RouteLocationNormalized,
    next: NavigationGuardNext
) => {
    const token = cookies.get('token')

    if (token) {
        if (to.path === '/login') {
            next({name: 'dashboard'})
            return
        }
    } else {
        if (to.path !== '/login') {
            next({name:'login-form'})
            return
        }
    }

    next()
}