<template>
  <q-form
    class="q-px-xl q-mb-xs"
    style="text-align: center; max-width: 500px; margin: 0 auto"
    @submit="onSubmit"
    @reset="onReset"
  >
    <h2 style="font-weight: 800">
      Sign In
    </h2>

    <q-input
      v-model="email"
      outlined
      label="E-mail"
      lazy-rules
      class="inputfield"
      :rules="[
        (val) => (val && val.length > 0) || 'Please enter your email address.',
      ]"
    />

    <q-input
      v-model="password"
      class="shadowtest"
      outlined
      :type="isPwd ? 'password' : 'text'"
      label="Password"
      lazy-rules
      :rules="[(val) => (val && val.length > 0) || 'Please enter a password.']"
    >
      <template #append>
        <q-icon
          :name="isPwd ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="isPwd = !isPwd"
        />
      </template>
    </q-input>
    <label class="fpwd cursor-pointer underlined">Forgot your password?</label>
    <br>

    <btn
      color="primary"
      label="Sign in"
      type="submit"
      size="md"
      class="q-mx-md cornered"
      glow-color="#00F1AF"
    />
    <!--     <br/> -->
    <label class="text-bold">or</label>

    <GitHubSignInButton />
    <q-separator class="sep middle-sep q-my-md" />
    <router-link
      :to="{ name: 'Signup' }"
      :class="q.dark.isActive ? 'text-white' : 'text-black'"
    >
      Sign Up
    </router-link>
  </q-form>
</template>

<script lang="ts">
import {useAuthenticationStore} from "../../stores/useAuthenticationStore"
import { useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue'
import { useMeta } from 'quasar'
import GitHubSignInButton from './components/GitHubSignInButton.vue'
import router from "../../router/index"
const metaData = {
  title: 'Sign In',
}
export default defineComponent({
  components: { GitHubSignInButton },
  setup() {
    const authenticationStore = useAuthenticationStore()
    const q = useQuasar()
    const email = ref('')
    const password = ref('')
    useMeta(metaData)
    return {
      email,
      password,
      isPwd: ref(true),
      onSubmit() {
        authenticationStore.login({email: email.value, password: password.value})
          .then(() => {
            router.push('/students') 
            
            q.notify({
              icon: 'done',
              color: 'positive',
              message: 'Submitted',
            })
          }).catch(() => {
            q.notify({
              icon: 'close',
              color: 'negative',
              message: 'Could not log in',
            })
          })
      },
      onReset() {
        email.value = ''
        password.value = ''
      },
    }
  },
})
</script>

<style scoped>

.sep {
  margin-left: 10em;
  margin-right: 10em;
}
:deep(.q-field__control) {
  border-radius: 14px !important;
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}
</style>

<style>
.underlined {
  text-decoration: underline;
}
.router-link {
  color: inherit;
}

.cornered {
  border-radius: 10px !important;
}
.fpwd {
  float: right;
  position: absolute;
  top: 250px;
  right: 50px;
  font-size: 80%;
}
</style>
