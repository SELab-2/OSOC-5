<template>
  <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-px-md q-mb-lg"
      style="text-align: center; max-width: 500px; margin: 0 auto;"
  >
    <h2  style="font-weight: 800">Sign In</h2>

    <q-input
        bg-color="brandteal"
        outlined
        v-model="email"
        label="E-mail"
        lazy-rules
        class="inputfield"
        :rules="[
           (val) => (val && val.length > 0) || 'Please enter your email address.',
        ]"
    />

    <q-input
        bg-color="brandteal"
        class="shadowtest"
        outlined
        :type="isPwd ? 'password' : 'text'"
        v-model="password"
        label="Password"
        lazy-rules
        :rules="[
           (val) => (val && val.length > 0) || 'Please enter a password.',
        ]"
    >
      <template v-slot:append>
        <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
        />
      </template>
    </q-input>
    <label class="fpwd cursor-pointer underlined">Forgot your password?</label>
    <br/>

    <div>
      <q-btn
          color="test"
          
          label="Sign in"
          type="submit"
          size="md"
          text-color="black"
          class="q-mx-md cornered"
      />
      <label class="text-bold">or</label>
      <q-btn round color="black" class="q-mx-md cursor-pointer cornered">
        <q-avatar size="35px" icon="mdi-github">
        </q-avatar>
      </q-btn>
      
      <q-separator class="sep middle-sep q-my-md"/>
      <router-link  class="underlined router-link" to="/signup">Sign Up</router-link>
    </div>
  </q-form>
</template>

<script>
import {useQuasar} from 'quasar'
import {ref} from 'vue'
import { useMeta } from 'quasar'

const metaData = {
  title: 'Sign In',
}

export default {
  setup() {
    const $q = useQuasar()

    const email = ref(null)
    const password = ref(null)
    
    useMeta(metaData)

    return {
      email,
      password,
      isPwd: ref(true),

      onSubmit() {
        $q.notify({
          icon: 'done',
          color: 'positive',
          message: 'Submitted'
        })
      },

      onReset() {
        email.value = null
        password.value = null
      }
    }
  },
}
</script>

<style scoped>
.sep {
  margin-left: 13em;
  margin-right: 13em;
}





</style>

<style>

body {
  background: #e8fff6;
}

.q-field__control {
  border-radius: 14px !important;
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

.bg-brandteal {
  background: #defff1 !important;
}

.bg-test {
  background: #f0faf6 !important;
}

.cornered {
  border-radius: 10px !important;
}

.fpwd {
  float: right;
  position: absolute;
  top: 250px;
  right: 15px;
  font-size: 80%;
}
</style>