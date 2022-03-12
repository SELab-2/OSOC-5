<template>
  <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-px-xl q-mb-xs"
      style="text-align: center; max-width:500px; margin: 0 auto;"
  >
    <h2  style="font-weight: 800">Sign In</h2>

    <q-input
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

<!--     <div> -->
      <q-btn
          color="primary"
          label="Sign in"
          type="submit"
          size="md"
          class="q-mx-md cornered"
          
      />
<!--     <br/> -->
      <label class="text-bold">or</label>
<!--       <br/> -->
      <q-btn
       color="black" 
       icon="mdi-github" 
       label="Sign in via GitHub" 
       class="q-mx-md cursor-pointer cornered"
       >
      </q-btn>
      
      <q-separator class="sep middle-sep q-my-md"/>
      <router-link  class="underlined router-link" to="/signup">Sign Up</router-link>
<!--     </div> -->
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
  margin-left: 10em;
  margin-right: 10em;
}
</style>

<style>

.q-field__control {
  border-radius: 14px !important;
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
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