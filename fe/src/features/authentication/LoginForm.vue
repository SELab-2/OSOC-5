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

    <btn
      class="q-mt-md"
      color="primary"
      label="Sign in"
      type="submit"
      glow-size="800px"
      glow-color="#00F1AF"
      
    />
  </q-form>
</template>

<script lang="ts">
import {useAuthenticationStore} from "../../stores/useAuthenticationStore"
import { useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue'
import { useMeta } from 'quasar'
import router from "../../router/index"
const metaData = {
  title: 'Sign In',
}
export default defineComponent({
  setup() {
    const authenticationStore = useAuthenticationStore()

    authenticationStore.checkLogin()

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

.fpwd {
  float: right;
  position: absolute;
  top: 250px;
  right: 50px;
  font-size: 80%;
}

.q-field__control {
  border-radius: 10px !important;
}
</style>
