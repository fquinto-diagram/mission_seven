<template>
<form @submit.prevent="handleSubmit" class="flex flex-col bg-zinc-200/40 text-black p-5 rounded-3xl mx-auto">
    <h1 class="mx-auto text-3xl font-bold ">LogIn</h1>
    <div class="flex flex-col">
        <MyInput
        placeholder="Email"
        class="bg-white mx-auto my-4"
        v-model="email"
        required
        />
        <MyInput
        class="bg-white mx-auto my-4"
        placeholder="Contrasenya"
        v-model="password"
        type="password"
        required
        />
        <MyButton
        class="text-black px-4 mx-auto"
        text="Enviar"
        style="cursor: pointer;"
        />
    </div>
    <div v-if="error" class="error">
        <span>{{ error }}</span>
    </div>
</form>
</template>

<script setup lang="ts">
import MyButton from '@/modules/common/components/MyButton.vue';
import MyInput from '@/modules/common/components/MyInput.vue';
// import { useAuthStore } from '@/modules/auth/store/storeCredentials';
import { postUser } from '@/modules/auth/helpers/postUser';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCookies }from 'vue3-cookies'

const router = useRouter();
const {cookies} = useCookies();

const email = ref('')
const password = ref('')
const error = ref('')

const handleSubmit = async ()=>{
    const credentials = {email: email.value, password: password.value};
    try {
        await postUser(credentials)
        const token = cookies.get('token')
        if(token){
            router.push({name: 'dashboard'})
        }else{
            alert(`Hay un erorr en con tu token`)
        }
    } catch (e: any) {
        error.value = e.message
    }
}

</script>