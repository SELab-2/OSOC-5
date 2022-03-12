<template>
  <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-px-md q-mb-lg"
      style="text-align: center; max-width: 500px; margin: 0 auto;"
  >
    <h3 class="text-bold">Sign Up</h3>

    <div class="row" >
      <div class="q-pr-xs col-6">
        <q-input
            filled
            v-model="firstName"
            label="First Name"
            lazy-rules
            :rules="[
           (val) => (val && val.length > 0) || 'Please enter your first name.',
        ]"
        />
      </div>

      <div class="q-pl-xs col-6">
        <q-input
            filled
            v-model="lastName"
            label="Last Name"
            lazy-rules
            :rules="[
           (val) => (val && val.length > 0) || 'Please enter your last name.',
        ]"
        />
      </div>
    </div>

    <q-input
        filled
        v-model="email"
        label="E-mail"
        type="email"
        lazy-rules
        :rules="[
           (val) => (val && val.length > 0) || 'Please enter your email address.',
        ]"
    />

    <q-input
        class="move-up"
        filled
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
    <q-input
        class="move-up"
        filled
        :type="isConfPwd ? 'password' : 'text'"
        v-model="confirmPassword"
        label="Confirm Password"
        lazy-rules
        :rules="[
           (val) => (val && val.length > 0) || 'Please confirm password.',
        ]"
    >
      <template v-slot:append>
        <q-icon
            :name="isConfPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isConfPwd = !isConfPwd"
        />
      </template>
    </q-input>

    <q-checkbox right-label size="xs" v-model="accept" label="I accept the license and terms" />

    <br/>

    <div>
      <q-btn
          label="Sign up"
          type="submit"
          size="md"
          color="white"
          text-color="black"
          class="q-mx-md"
      />
      <label class="text-bold">or</label>
      <q-icon name="mdi-github" size="2.5em" class="q-mx-md cursor-pointer"/>
      <q-separator inset class="middle-sep q-my-md"/>
      <router-link :to="{ name: 'Login' }" :class="$q.dark.isActive ? 'text-white' : 'text-black'" >Log In</router-link>
    </div>
  </q-form>
</template>

<script>
import {useQuasar} from 'quasar'
import {ref} from 'vue'

export default {
  setup() {
    const $q = useQuasar()

    const email = ref(null)
    const firstName = ref(null)
    const lastName = ref(null)
    const password = ref(null)
    const confirmPassword = ref(null)
    const accept = ref(true)

    return {
      email,
      firstName,
      lastName,
      password,
      confirmPassword,
      accept,
      isPwd: ref(true),
      isConfPwd: ref(true),

      onSubmit () {
        if (password.value !== confirmPassword.value) {
          $q.notify({
            color: 'negative',
            message: 'Passwords do not match'
          })
        } else if (accept.value !== true) {
          $q.notify({
            color: 'negative',
            message: 'You need to accept the license and terms first'
          })
        }
        else {
          $q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Submitted'
          })
        }
      },

      onReset() {
        email.value = null
        password.value = null
      }
    }
  },
}
</script>

<style>
.underlined {
  text-decoration: underline;
}

.router-link {
  color: inherit;
}
</style>