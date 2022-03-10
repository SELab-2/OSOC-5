<template>
  <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-px-md q-mb-lg"
      style="text-align: center; max-width: 500px; margin: 0 auto;"
  >
    <h3 class="text-bold">Login</h3>
    <q-input
        filled
        v-model="email"
        label="E-mail"
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
    <label class="fpwd cursor-pointer underlined">Forgot your password?</label>
    <br />

    <div>
      <q-btn
          rounded
          label="Log in"
          type="submit"
          size="md"
          color="white"
          text-color="black"
          class="q-mx-md"
      />
      <label class="text-bold">or</label>
      <q-icon name="mdi-github" size="2.5em" class="q-mx-md cursor-pointer" />
      <q-separator inset class="middle-sep q-my-md" />
      <label class="underlined cursor-pointer q-my-md">Signup</label>
    </div>
  </q-form>
</template>

<script>
import { useQuasar } from 'quasar'
import { ref } from 'vue'

export default {
  setup() {
    const $q = useQuasar()

    const email = ref(null)
    const password = ref(null)

    return {
      email,
      password,
      isPwd: ref(true),

      onSubmit() {
        $q.notify({
          color: 'green-4',
          textColor: 'white',
          icon: 'cloud_done',
          message: 'Submitted',
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

<style>
.underlined {
  text-decoration: underline;
}

.fpwd {
  float: right;
  position: absolute;
  top: 235px;
  right: 15px;
  font-size: 80%;
}
</style>