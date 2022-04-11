<template>
  <q-form
      @submit="onSubmit"
      @reset="onReset"

      class="q-px-xl q-mb-lg"
      style="text-align: center; max-width: 500px; margin: 0 auto; margin-top: 7em;"
  >
    <h2 style="font-weight: 800">Sign Up</h2>

    <div class="row" >
      <div class="q-pr-xs col-6">
        <q-input


            outlined
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
            outlined
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
        outlined
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
    <q-input
        class="move-up"
        outlined
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


    <q-checkbox v-model="accept" label="I accept the terms and conditions." />
    <br/>

    <div>
      <btn
         label="Sign up"
         type="submit"
         size="md"
         color="primary"
         class="q-mx-md cornered"
         glow-color="#00FFB5"
      />
      <label class="text-bold">or</label>
      <GitHubSignInButton/>

      <q-separator inset class="middle-sep q-my-md sep"/>
      <router-link :to="{ name: 'Login' }" :class="$q.dark.isActive ? 'text-white' : 'text-black'" >Log In</router-link>
    </div>
  </q-form>
</template>

<script lang="ts">
import {useQuasar} from 'quasar'
import {defineComponent, ref} from 'vue'
import { useMeta } from 'quasar'
import GitHubSignInButton from './components/GitHubSignInButton.vue'
const metaData = {
  title: 'Sign Up',
}
export default defineComponent({
  components: { GitHubSignInButton },
  setup() {
    const $q = useQuasar()
    const email = ref(null)
    const firstName = ref(null)
    const lastName = ref(null)
    const password = ref(null)
    const confirmPassword = ref(null)
    const accept = ref(false)

    useMeta(metaData)

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
})
</script>


<style scoped>
.sep {
  margin-left: 10em;
  margin-right: 10em;
}
:deep(.q-field__control) {
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}
</style>

<style>
.q-field__control {
  border-radius: 10px !important;
}

.underlined {
  text-decoration: underline;
}
.q-checkbox__bg {
  border-radius: 6px !important;
}
.router-link {
  color: inherit;
}
</style>