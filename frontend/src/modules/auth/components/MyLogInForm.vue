<template>
<form @submit.prevent="handleSubmit" class="flex flex-col bg-zinc-200/40 text-black p-5 rounded-3xl mx-auto">
    <h1 class="mx-auto text-3xl font-bold ">LogIn</h1>
    <div class="flex flex-col">
        <MyInput
        placeholder="Email"
        class="bg-white mx-auto my-4"
        type="email"
        v-model="credentials.email"
        required
        />
        <MyInput
        class="bg-white mx-auto my-4"
        placeholder="Contrasenya"
        type="password"
        v-model="credentials.password"
        required
        />
        <MyButton
        class="text-white mx-auto"
        text="Enviar"
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
import { useLogin } from '@/modules/auth/composables/useValidateForm';
import { useRouter } from 'vue-router';
import { ref, reactive } from 'vue';
import type { LoginCredentials } from '@/modules/auth/interface/validateForm.inteface';

const error = ref('')
const isLoading = ref(false)
const router = useRouter()

const credentials = reactive<LoginCredentials>({
    email: '',
    password: ''
});

async function handleSubmit(){
    try{
        console.log(credentials)
        isLoading.value= true
        error.value= ''
        const response= await useLogin(credentials)
        if(response?.token){
            router.push({name: 'dashboard'})
        }else{
            alert(`U`)
        }
    }catch(e: any){
        error.value = e.message
        alert(`AAAA: \n ${e}`)
    }finally{
        isLoading.value= false
    }
}
</script>