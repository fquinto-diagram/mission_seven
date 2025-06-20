import { useAuthStore } from "@/modules/auth/store/storeCredentials"
import { useRouter } from "vue-router"

export default {
  setup() {
    const userStore = useAuthStore()
    const router = useRouter()

    const handleLogout = async () => {
      await userStore.logOut()
      router.push({name: 'login'}) // o la ruta que corresponda
    }

    return {
      handleLogout
    }
  }
}