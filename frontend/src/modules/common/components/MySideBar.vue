<template>
    <aside class="fixed left-0 top-20 h-[calc(100vh-5rem)] bg-gray-100 border-r-2 border-gray-200 transition-all duration-300 w-16 min-w-[56px] md:min-w-[180px] flex flex-col items-center md:items-stretch z-40">
        <div class="h-full w-full px-1 md:px-3 py-4 overflow-y-auto flex flex-col gap-4">
            <router-link v-for="route in routes" :to="{ name: route.route}" 
            class="flex p-2 hover:bg-gray-200 ">
                <span style="cursor: pointer;" v-html="route.icon"></span><span class="capitalize">{{ route.name }}</span>
            </router-link>
        </div>
    </aside>
</template>

<script setup lang="ts">

const routes = [
    {
        route: 'dashboard',
        name: 'dashboard',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3L2 12h3v8z"/></svg>`,
    },
    {
        route: 'profile-form',
        name: 'Perfils',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12c5.16-1.26 9-6.45 9-12V5zm0 4a3 3 0 0 1 3 3a3 3 0 0 1-3 3a3 3 0 0 1-3-3a3 3 0 0 1 3-3m5.13 12A9.7 9.7 0 0 1 12 20.92A9.7 9.7 0 0 1 6.87 17c-.34-.5-.63-1-.87-1.53c0-1.65 2.71-3 6-3s6 1.32 6 3c-.24.53-.53 1.03-.87 1.53"/></svg>`,
    },
    // {
    //     route: '',
    //     name: 'roles',
    //     icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 5.5A3.5 3.5 0 0 1 15.5 9a3.5 3.5 0 0 1-3.5 3.5A3.5 3.5 0 0 1 8.5 9A3.5 3.5 0 0 1 12 5.5M5 8c.56 0 1.08.15 1.53.42c-.15 1.43.27 2.85 1.13 3.96C7.16 13.34 6.16 14 5 14a3 3 0 0 1-3-3a3 3 0 0 1 3-3m14 0a3 3 0 0 1 3 3a3 3 0 0 1-3 3c-1.16 0-2.16-.66-2.66-1.62a5.54 5.54 0 0 0 1.13-3.96c.45-.27.97-.42 1.53-.42M5.5 18.25c0-2.07 2.91-3.75 6.5-3.75s6.5 1.68 6.5 3.75V20h-13zM0 20v-1.5c0-1.39 1.89-2.56 4.45-2.9c-.59.68-.95 1.62-.95 2.65V20zm24 0h-3.5v-1.75c0-1.03-.36-1.97-.95-2.65c2.56.34 4.45 1.51 4.45 2.9z"/></svg>`,
    // },
    {
        route: 'roles-form',
        name: 'crear roles',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M3 3v19l3-2l3 2l3-2l1.3.86c-.2-.58-.3-1.21-.3-1.86a6.005 6.005 0 0 1 8-5.66V3zm14 4v2H7V7zm-2 4v2H7v-2zm3 4v3h-3v2h3v3h2v-3h3v-2h-3v-3z"/></svg>`,
    },
    {
        route: 'roles-list',
        name: 'Lista de Roles',
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M7 5h15v16l-2.5-1.68L17 21l-2.5-1.68L12 21l-2.5-1.68L7 21zm11 4h-7v2h7zm-7 4v2h5v-2zM3 7c-.6 0-1 .4-1 1s.4 1 1 1h2V7zm-2 5c0-.6.4-1 1-1h3v2H2c-.6 0-1-.4-1-1m0 3c-.6 0-1 .4-1 1s.4 1 1 1h4v-2z"/></svg>`
    }


]
</script>